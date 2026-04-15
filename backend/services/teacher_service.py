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

        # 4. Translation (Eng→Arabic)
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


def generate_dataset_task(
    limit: int | None = None,
    article_ids: list[str] | None = None,
):
    """Background task to generate dataset for pending articles.

    If article_ids is provided, only those specific articles are processed
    (regardless of status). Otherwise, processes all PENDING articles up to limit.
    """
    from database import SessionLocal
    db = SessionLocal()
    try:
        if article_ids:
            articles = db.query(Article).filter(Article.id.in_(article_ids)).all()
            # Preserve the order requested by caller
            id_order = {aid: i for i, aid in enumerate(article_ids)}
            articles.sort(key=lambda a: id_order.get(a.id, 9999))
        else:
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


# --- BATCH GENERATION (Anthropic Messages Batches API) ---

def _build_teacher_batch_items(articles: list[Article]) -> list[dict]:
    """Build batch items for all 4 tasks × N articles.
    Returns items in the format expected by build_anthropic_batch_requests.
    custom_id format: '{article_id}:{task}' where task ∈ {ner, summary, nli, translation}
    """
    items = []
    for art in articles:
        body = art.body
        items.append({
            "custom_id": f"{art.id}__ner",
            "system": NER_SYSTEM,
            "user": NER_USER.format(article_body=body),
        })
        items.append({
            "custom_id": f"{art.id}__summary",
            "system": SUMMARY_SYSTEM,
            "user": SUMMARY_USER.format(article_body=body),
        })
        items.append({
            "custom_id": f"{art.id}__nli",
            "system": NLI_SYSTEM,
            "user": NLI_USER.format(article_body=body),
        })
        items.append({
            "custom_id": f"{art.id}__translation",
            "system": TRANSLATION_SYSTEM,
            "user": TRANSLATION_USER.format(article_body=body),
        })
    return items


def _apply_teacher_batch_results(
    articles: list[Article],
    results: dict[str, dict],
    db: Session,
    teacher_model: str,
):
    """Parse batch results and write DatasetItems to DB."""
    from datetime import datetime as _dt
    for art in articles:
        try:
            ner_text = (results.get(f"{art.id}__ner") or {}).get("text", "")
            summary_text = (results.get(f"{art.id}__summary") or {}).get("text", "")
            nli_text = (results.get(f"{art.id}__nli") or {}).get("text", "")
            trans_text = (results.get(f"{art.id}__translation") or {}).get("text", "")

            # Parse JSON-mode tasks
            ner_ref = parse_json_response(ner_text) if ner_text else {}
            nli_claims = unwrap_json_list(parse_json_response(nli_text)) if nli_text else []
            try:
                trans_data = parse_json_response(trans_text) if trans_text else {}
            except Exception:
                trans_data = {}

            item = db.query(DatasetItem).filter(DatasetItem.article_id == art.id).first()
            if not item:
                item = DatasetItem(article_id=art.id)
                db.add(item)

            item.ner_input = art.body
            item.ner_reference = ner_ref
            item.summary_input = art.body
            item.summary_reference = (summary_text or "").strip()
            item.nli_input = art.body
            item.nli_claims = nli_claims
            item.translation_input = trans_data.get("english_source", "") if isinstance(trans_data, dict) else ""
            item.translation_reference = trans_data.get("arabic_translation", "") if isinstance(trans_data, dict) else ""
            item.generated_at = _dt.utcnow()
            item.teacher_model = teacher_model

            art.status = ArticleStatus.READY
            db.commit()
        except Exception as e:
            print(f"[Teacher batch] ERROR applying {art.id}: {e}")
            art.status = ArticleStatus.ERROR
            db.commit()


def generate_dataset_batch(article_ids: list[str], poll_interval: int = 30):
    """Generate all 4 dataset tasks for a list of articles using Anthropic Batch API.

    50% cost discount vs sync. Typical completion: 5-30 min for ~100 articles.
    """
    from database import SessionLocal
    from services.batch_anthropic import (
        build_anthropic_batch_requests,
        submit_anthropic_batch,
        wait_for_anthropic_batch,
        download_anthropic_batch_results,
    )

    db = SessionLocal()
    try:
        api_key = settings.get_teacher_api_key()
        model = settings.TEACHER_MODEL

        articles = db.query(Article).filter(Article.id.in_(article_ids)).all()
        id_order = {aid: i for i, aid in enumerate(article_ids)}
        articles.sort(key=lambda a: id_order.get(a.id, 9999))

        if not articles:
            print("[Teacher batch] No articles to process")
            return

        # Mark all as GENERATING
        for art in articles:
            art.status = ArticleStatus.GENERATING
        db.commit()

        print(f"[Teacher batch] Building batch for {len(articles)} articles × 4 tasks = {len(articles)*4} requests")
        items = _build_teacher_batch_items(articles)
        requests = build_anthropic_batch_requests(model=model, items=items)

        print(f"[Teacher batch] Submitting batch...")
        batch_id = submit_anthropic_batch(api_key=api_key, requests=requests)
        print(f"[Teacher batch] Submitted: {batch_id}")

        def progress(status):
            counts = status.get("request_counts", {})
            print(f"[Teacher batch] {status['processing_status']}: "
                  f"succeeded={counts.get('succeeded', 0)} "
                  f"errored={counts.get('errored', 0)} "
                  f"processing={counts.get('processing', 0)}")

        wait_for_anthropic_batch(
            api_key=api_key, batch_id=batch_id,
            poll_interval=poll_interval, progress_callback=progress,
        )

        print(f"[Teacher batch] Downloading results...")
        results = download_anthropic_batch_results(api_key=api_key, batch_id=batch_id)
        print(f"[Teacher batch] Got {len(results)} results")

        _apply_teacher_batch_results(articles, results, db, teacher_model=model)
        ready = sum(1 for a in articles if a.status == ArticleStatus.READY)
        print(f"[Teacher batch] {ready}/{len(articles)} articles READY")

    finally:
        db.close()
