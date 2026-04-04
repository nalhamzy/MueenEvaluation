"""Teacher LLM service - generates dataset items from articles."""

from datetime import datetime
from sqlalchemy.orm import Session
from models import Article, DatasetItem, ArticleStatus
from services.llm_client import call_llm, parse_json_response, unwrap_json_list
from config import settings


# --- Prompts from spec ---

NER_SYSTEM = """You are an expert Arabic NLP annotator. Your output must be valid JSON only.
No preamble. No markdown fences. No explanation."""

NER_USER = """Given the following Arabic news article, extract all named entities and return
a JSON object with exactly these four keys:
  "PERSON"       — named individuals only (not titles like وزير or رئيس alone)
  "LOCATION"     — geographic places, border crossings, regions, bodies of water
  "ORGANIZATION" — government bodies, militias, companies, agencies
  "MISC"         — weapons, equipment, vehicles, numbered quantities of physical items

Rules:
1. Extract only entities that appear in the text. Do not infer or add entities not present.
2. For PERSON: include full name as it appears. Do not extract generic titles without a name.
3. For ORGANIZATION: if an organization has both an Arabic name and an acronym in the text,
   list the full name only. Do not duplicate as two entries.
4. For LOCATION: if the same place is described with varying specificity
   (e.g. "منفذ صرفيت" and "منفذ صرفيت بمحافظة المهرة"), list the most specific form.
5. Deduplicate: do not list morphological variants (definite/indefinite) as separate entities.
6. Return JSON only. No other text.

Article:
{article_body}"""

SUMMARY_SYSTEM = """You are an expert Arabic news analyst. Write only in formal Modern Standard Arabic (فصحى).
No dialect. No code-switching. No English words. Output the summary only — no labels,
no preamble."""

SUMMARY_USER = """Summarize the following Arabic news article in exactly 2 sentences in formal Arabic (فصحى).

Rules:
1. Do not copy any sentence verbatim from the source. Rephrase all content.
2. Cover the most important events. Prioritize named actors, locations, and actions.
3. Do not add analysis, conclusions, or opinions not explicitly stated in the article.
   (Do not write phrases like "مما يعكس..." or "وهو ما يدل على..." unless sourced.)
4. Maintain formal register throughout. No colloquial expressions.
5. Do not mention the word "المقال" or "التقرير" — write as if briefing a colleague directly.

Article:
{article_body}"""

NLI_SYSTEM = """You are an expert fact-checking annotator for Arabic news. Output valid JSON only.
No markdown. No preamble."""

NLI_USER = """Given the following Arabic news article, generate exactly 4 claim-label pairs for
a Natural Language Inference (NLI) fact-verification benchmark.

Requirements:
- Exactly 2 claims labelled "SUPPORTED" (clearly supported by the text)
- Exactly 1 claim labelled "REFUTED" (directly contradicted by the text)
- Exactly 1 claim labelled "NOT_ENOUGH_INFO" (plausible but not confirmed by the text)

Hard rules:
1. All claims must be written in Arabic.
2. The REFUTED claim must be a subtle distortion of a fact in the text
   (e.g. wrong number, wrong location, wrong actor) — not an obvious fabrication.
3. The NOT_ENOUGH_INFO claim must be plausible and related to the article's topic
   but genuinely absent from the text.
4. Do not use phrases from the article verbatim in the claims — paraphrase.
5. Return JSON array: [{{"claim": "...", "label": "SUPPORTED|REFUTED|NOT_ENOUGH_INFO"}}, ...]

Article:
{article_body}"""

COREF_SYSTEM = """You are an expert Arabic NLP annotator specializing in entity coreference resolution.
Your output must be valid JSON only. No preamble. No markdown fences. No explanation."""

COREF_USER = """Given the following Arabic news article, identify all referring expressions for
key named entities mentioned multiple times. For each mention, identify:
1. The exact text span as it appears in the article
2. The referent — what real-world entity or concept it refers to, with disambiguation
   (e.g. which side of a border crossing, which political faction, which specific person)
3. The paragraph number (1-indexed) where the span appears

Focus on entities that are referred to in multiple ways or that could be ambiguous.
Include pronouns, definite descriptions, and partial names that refer to previously
mentioned entities.

Return a JSON array:
[
  {{
    "span": "exact Arabic text span",
    "referent": "clear English description of what this refers to",
    "paragraph": integer
  }},
  ...
]

Rules:
1. Only include spans that actually appear in the text.
2. The referent must disambiguate — if two entities share a name or description,
   clarify which one is meant.
3. Include at least 3 referring expressions.
4. Group related mentions — if the same entity is mentioned 3 times, list all 3.
5. Return JSON only. No other text.

Article:
{article_body}"""

TRANSLATION_SYSTEM = """You are an expert English-to-Arabic translator. Write only in formal Modern Standard Arabic (فصحى).
No dialect. No code-switching. Output the translation only — no labels, no preamble."""

TRANSLATION_USER = """Given the following Arabic news article, first generate a 3-sentence English summary
of the article's key events, then provide a gold-standard Arabic translation of that summary.

Rules:
1. The English summary must capture the main actors, locations, and events.
2. The Arabic translation must be in formal MSA (فصحى) — no dialect.
3. The translation must be faithful to the English — no added information.
4. Use proper Arabic punctuation and grammar.
5. Return ONLY a JSON object with two keys: "english_source" and "arabic_translation".

Article:
{article_body}"""


def generate_for_article(article: Article, db: Session) -> DatasetItem:
    """Generate all 5 dataset tasks for a single article using the Teacher LLM."""
    api_key = settings.get_teacher_api_key()
    model = settings.TEACHER_MODEL
    base_url = settings.OPENAI_BASE_URL

    article.status = ArticleStatus.GENERATING
    db.commit()

    try:
        # 1. NER
        ner_raw = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=NER_SYSTEM,
            user_prompt=NER_USER.format(article_body=article.body),
            json_mode=True, db=db, task_type="teacher_ner",
        )
        ner_reference = parse_json_response(ner_raw)

        # 2. Summary
        summary_reference = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=SUMMARY_SYSTEM,
            user_prompt=SUMMARY_USER.format(article_body=article.body),
            db=db, task_type="teacher_summary",
        )

        # 3. NLI
        nli_raw = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=NLI_SYSTEM,
            user_prompt=NLI_USER.format(article_body=article.body),
            json_mode=True, db=db, task_type="teacher_nli",
        )
        nli_claims = unwrap_json_list(parse_json_response(nli_raw))

        # 4. Coreference Resolution
        coref_raw = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=COREF_SYSTEM,
            user_prompt=COREF_USER.format(article_body=article.body),
            json_mode=True, db=db, task_type="teacher_coref",
        )
        coref_reference = unwrap_json_list(parse_json_response(coref_raw))

        # 5. Translation (Eng→Arabic)
        translation_raw = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=TRANSLATION_SYSTEM,
            user_prompt=TRANSLATION_USER.format(article_body=article.body),
            json_mode=True, db=db, task_type="teacher_translation",
        )
        translation_data = parse_json_response(translation_raw)

        # Create or update DatasetItem
        item = db.query(DatasetItem).filter(DatasetItem.article_id == article.id).first()
        if not item:
            item = DatasetItem(article_id=article.id)
            db.add(item)

        item.ner_input = article.body
        item.ner_reference = ner_reference
        item.summary_input = article.body
        item.summary_reference = summary_reference.strip()
        item.nli_input = article.body
        item.nli_claims = nli_claims
        item.coref_input = article.body
        item.coref_reference = coref_reference
        item.translation_input = translation_data.get("english_source", "")
        item.translation_reference = translation_data.get("arabic_translation", "")
        item.generated_at = datetime.utcnow()
        item.teacher_model = model

        article.status = ArticleStatus.READY
        db.commit()
        db.refresh(item)
        return item

    except Exception as e:
        article.status = ArticleStatus.ERROR
        db.commit()
        raise e


def generate_dataset_task(limit: int | None = None):
    """Background task to generate dataset for all pending articles."""
    from database import SessionLocal
    db = SessionLocal()
    try:
        query = db.query(Article).filter(Article.status == ArticleStatus.PENDING)
        if limit:
            query = query.limit(limit)
        articles = query.all()

        for article in articles:
            try:
                generate_for_article(article, db)
                print(f"[Teacher] Generated dataset for {article.id}")
            except Exception as e:
                print(f"[Teacher] ERROR on {article.id}: {e}")
    finally:
        db.close()
