"""Manual evaluation run service.

Allows users to evaluate any browser-based LLM (Cursor, ChatGPT web, Claude.ai, etc)
without needing an API key:

  1. User picks N articles → server generates a markdown "task brief"
  2. User pastes the brief into their browser assistant
  3. The assistant produces a structured JSON file with outputs for all 4 tasks
  4. User uploads the JSON → server creates a run, parses and scores the outputs

The 4 tasks are NER, Summary, NLI, Translation. Each output is scored using
the same logic as a regular run (NER/NLI deterministic, Summary/Translation via
LLM-as-judge if available).
"""

from datetime import datetime
from sqlalchemy.orm import Session

from models import (
    Article, DatasetItem, EvaluationRun, ModelOutput,
    RunStatus, OutputStatus,
)


# --- Brief generation ---

BRIEF_HEADER = """# Arabic LLM Benchmark — Manual Evaluation Brief

You are evaluating an LLM on Arabic NLP tasks. For each article below, perform 4 tasks
and return a single JSON object with the results.

## Tasks (per article)

1. **NER** — Extract named entities into 4 categories: PERSON, LOCATION, ORGANIZATION, MISC
2. **SUMMARY** — Write a 2-sentence summary in formal Modern Standard Arabic (فصحى).
   Do not copy verbatim from the source. Maintain formal register throughout.
3. **NLI** — For each provided claim, label it as SUPPORTED, REFUTED, or NOT_ENOUGH_INFO
   based solely on the article body.
4. **TRANSLATION** — Translate the provided English text to formal Arabic (فصحى).
   Be faithful to the source. No additions, no omissions, no dialect.

## Output format

Return ONE JSON object (and nothing else) with this exact structure:

```json
{
  "model_name": "<your-model-name-here>",
  "outputs": [
    {
      "article_id": "ARTICLE_ID_HERE",
      "ner_output": {
        "PERSON": ["..."],
        "LOCATION": ["..."],
        "ORGANIZATION": ["..."],
        "MISC": ["..."]
      },
      "summary_output": "<2-sentence Arabic summary>",
      "nli_output": [
        {"claim": "<the same claim text>", "label": "SUPPORTED|REFUTED|NOT_ENOUGH_INFO"},
        ...
      ],
      "translation_output": "<Arabic translation>"
    },
    ...
  ]
}
```

**IMPORTANT**:
- Replace `<your-model-name-here>` with the model you used (e.g. "claude-opus-via-cursor")
- Use the EXACT article_id values from the brief below
- For NLI, return labels in the SAME order as the claims provided
- Do not include any text outside the JSON object
- Do not wrap the JSON in markdown code fences in your final answer

---

# Articles to evaluate

"""


def build_brief(article_ids: list[str], db: Session) -> str:
    """Generate a markdown task brief for the given article IDs.

    Each article must have a generated DatasetItem (NLI claims and translation
    input come from the dataset). Returns the full markdown text.
    """
    items = (
        db.query(DatasetItem)
        .filter(DatasetItem.article_id.in_(article_ids))
        .filter(DatasetItem.generated_at.isnot(None))
        .all()
    )
    if not items:
        raise ValueError("No DatasetItems found for the given article_ids")

    # Preserve requested order
    order = {aid: i for i, aid in enumerate(article_ids)}
    items.sort(key=lambda i: order.get(i.article_id, 9999))

    article_map = {
        a.id: a for a in db.query(Article).filter(Article.id.in_(article_ids)).all()
    }

    sections = [BRIEF_HEADER]

    for item in items:
        art = article_map.get(item.article_id)
        if not art:
            continue

        sections.append(f"## Article {item.article_id}\n")
        sections.append("### Article body (Arabic)\n")
        sections.append("```")
        sections.append(art.body)
        sections.append("```\n")

        # NLI claims to label
        if item.nli_claims:
            sections.append("### NLI claims to label")
            for i, claim in enumerate(item.nli_claims, start=1):
                claim_text = claim.get("claim", "") if isinstance(claim, dict) else str(claim)
                sections.append(f"{i}. {claim_text}")
            sections.append("")

        # English text to translate
        if item.translation_input:
            sections.append("### English text to translate to Arabic")
            sections.append("```")
            sections.append(item.translation_input)
            sections.append("```\n")

        sections.append("---\n")

    return "\n".join(sections)


# --- Upload + scoring ---

def create_manual_run(payload: dict, db: Session) -> dict:
    """Create a run from an uploaded outputs JSON and score it.

    Expected payload shape:
        {
          "model_name": "...",
          "outputs": [
            {
              "article_id": "...",
              "ner_output": {...},
              "summary_output": "...",
              "nli_output": [...],
              "translation_output": "..."
            },
            ...
          ]
        }

    Returns: {"run_id": str, "scored_count": int, "missing": list[str], "errors": list[str]}
    """
    from services.scoring_service import score_output

    model_name = (payload.get("model_name") or "manual-upload").strip()
    outputs_payload = payload.get("outputs") or []
    if not isinstance(outputs_payload, list) or not outputs_payload:
        raise ValueError("payload.outputs must be a non-empty list")

    article_ids = [o.get("article_id") for o in outputs_payload if o.get("article_id")]
    items_by_article = {
        item.article_id: item
        for item in db.query(DatasetItem)
        .filter(DatasetItem.article_id.in_(article_ids))
        .filter(DatasetItem.generated_at.isnot(None))
        .all()
    }

    # Create the run
    run = EvaluationRun(
        model_name=model_name,
        api_base_url="manual",
        status=RunStatus.RUNNING,
        total_articles=len(outputs_payload),
        started_at=datetime.utcnow(),
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    missing: list[str] = []
    errors: list[str] = []
    scored = 0

    for entry in outputs_payload:
        aid = entry.get("article_id")
        if not aid:
            errors.append("entry without article_id")
            continue

        item = items_by_article.get(aid)
        if not item:
            missing.append(aid)
            continue

        try:
            output = ModelOutput(
                run_id=run.id,
                dataset_item_id=item.id,
                article_id=aid,
                ner_output=entry.get("ner_output") or None,
                summary_output=entry.get("summary_output") or None,
                nli_output=entry.get("nli_output") or None,
                translation_output=entry.get("translation_output") or None,
                status=OutputStatus.PENDING,
                processed_at=datetime.utcnow(),
            )
            db.add(output)
            db.commit()
            db.refresh(output)

            # Score deterministically (NER + NLI). Summary/Translation will be 0
            # unless judge_run_task is invoked separately.
            score_output(output, db)
            scored += 1
        except Exception as e:
            errors.append(f"{aid}: {str(e)[:200]}")
            db.rollback()

    run.processed_count = scored
    run.completed_at = datetime.utcnow()
    run.status = RunStatus.COMPLETED if scored > 0 else RunStatus.FAILED
    db.commit()

    return {
        "run_id": run.id,
        "scored_count": scored,
        "missing": missing,
        "errors": errors,
    }
