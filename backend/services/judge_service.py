"""LLM Judge service - scores summary outputs (coref is now deterministic)."""

from sqlalchemy.orm import Session
from models import ModelOutput, DatasetItem, Article, OutputStatus
from services.llm_client import call_llm, parse_json_response
from services.scoring_service import (
    compute_summary_score_from_rubric,
    compute_translation_score_from_rubric,
    compute_overall_score,
)
from config import settings


# --- Judge prompt for summary ---

SUMMARY_JUDGE_SYSTEM = (
    "You are an expert evaluator of Arabic text summarization. "
    "Return valid JSON only. No preamble. No markdown."
)

SUMMARY_JUDGE_USER = """Score the following Arabic summary against the reference and source article.

SOURCE ARTICLE:
{article_body}

REFERENCE SUMMARY (gold standard):
{summary_reference}

MODEL SUMMARY (to evaluate):
{summary_output}

Return a JSON object with these exact keys:
{{
  "factual_accuracy":   integer 0-3,
  "coverage":           integer 0-3,
  "no_added_inference": integer 0-2,
  "register_fluency":   integer 0-2,
  "verbatim_penalty":   integer 0-1,
  "reasoning":          string
}}"""


def judge_summary(output: ModelOutput, db: Session) -> float:
    """Score a summary output using the LLM judge. Returns score 0-10."""
    item = db.query(DatasetItem).filter(DatasetItem.id == output.dataset_item_id).first()
    article = db.query(Article).filter(Article.id == output.article_id).first()

    if not output.summary_output or not item.summary_reference:
        return 0.0

    api_key = settings.get_judge_api_key()
    model = settings.JUDGE_MODEL

    raw = call_llm(
        api_key=api_key, model=model,
        base_url=settings.OPENAI_BASE_URL,
        system_prompt=SUMMARY_JUDGE_SYSTEM,
        user_prompt=SUMMARY_JUDGE_USER.format(
            article_body=article.body,
            summary_reference=item.summary_reference,
            summary_output=output.summary_output,
        ),
        json_mode=True, db=db, task_type="judge_summary",
    )

    rubric = parse_json_response(raw)
    output.judge_summary_rubric = rubric
    score = compute_summary_score_from_rubric(rubric)
    output.summary_score = score
    db.commit()
    return score


TRANSLATION_JUDGE_SYSTEM = (
    "You are an expert bilingual Arabic-English linguist and translation evaluator. "
    "Return valid JSON only. No preamble. No markdown."
)

TRANSLATION_JUDGE_USER = """Score the following Arabic translation against the reference and English source.

ENGLISH SOURCE:
{english_source}

REFERENCE TRANSLATION (gold standard):
{translation_reference}

MODEL TRANSLATION (to evaluate):
{translation_output}

Return a JSON object with these exact keys:
{{
  "faithfulness":       integer 0-3,  // 0=major omissions/additions, 1=some, 2=minor, 3=fully faithful
  "fluency":            integer 0-3,  // 0=broken Arabic, 1=awkward, 2=natural, 3=native-quality
  "terminology":        integer 0-2,  // 0=wrong terms, 1=acceptable, 2=precise domain terms
  "register":           integer 0-2,  // 0=dialect/casual, 1=mixed, 2=formal MSA throughout
  "reasoning":          string
}}"""


def judge_translation(output: ModelOutput, db: Session) -> float:
    """Score a translation output using the LLM judge. Returns score 0-10."""
    item = db.query(DatasetItem).filter(DatasetItem.id == output.dataset_item_id).first()

    if not output.translation_output or not item.translation_reference:
        return 0.0

    api_key = settings.get_judge_api_key()
    model = settings.JUDGE_MODEL

    raw = call_llm(
        api_key=api_key, model=model,
        base_url=settings.OPENAI_BASE_URL,
        system_prompt=TRANSLATION_JUDGE_SYSTEM,
        user_prompt=TRANSLATION_JUDGE_USER.format(
            english_source=item.translation_input,
            translation_reference=item.translation_reference,
            translation_output=output.translation_output,
        ),
        json_mode=True, db=db, task_type="judge_translation",
    )

    rubric = parse_json_response(raw)
    output.judge_translation_rubric = rubric
    score = compute_translation_score_from_rubric(rubric)
    output.translation_score = score
    db.commit()
    return score


def judge_output(output: ModelOutput, db: Session):
    """Run LLM judge for summary and translation, then recompute overall score."""
    try:
        judge_summary(output, db)
    except Exception as e:
        print(f"[Judge] Summary scoring failed for {output.id}: {e}")
        if output.summary_score is None:
            output.summary_score = 0.0

    try:
        judge_translation(output, db)
    except Exception as e:
        print(f"[Judge] Translation scoring failed for {output.id}: {e}")
        if output.translation_score is None:
            output.translation_score = 0.0

    # Recompute overall with all scores
    output.overall_score = compute_overall_score(
        output.ner_score or 0,
        output.nli_score or 0,
        output.summary_score or 0,
        output.coref_score or 0,
        output.translation_score or 0,
    )
    output.status = OutputStatus.SCORED
    db.commit()


def judge_run_task(run_id: str):
    """Background task: run LLM judge on all outputs for a run."""
    from database import SessionLocal
    db = SessionLocal()
    try:
        outputs = (
            db.query(ModelOutput)
            .filter(ModelOutput.run_id == run_id)
            .all()
        )
        for output in outputs:
            try:
                judge_output(output, db)
                print(f"[Judge] Scored {output.article_id} for run {run_id}")
            except Exception as e:
                print(f"[Judge] ERROR {output.article_id}: {e}")
    finally:
        db.close()
