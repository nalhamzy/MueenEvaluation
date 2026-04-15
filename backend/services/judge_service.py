"""LLM Judge service - scores summary and translation outputs."""

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


# --- BATCH JUDGE (OpenAI Batch API) ---

def judge_run_batch(run_id: str, poll_interval: int = 30):
    """Run LLM judge on all outputs for a run using OpenAI Batch API.

    50% cost discount vs sync. Builds 2 requests per output (summary + translation),
    submits as batch, polls until done, then writes scores back.
    """
    from database import SessionLocal
    from services.batch_openai import (
        build_openai_batch_line,
        submit_openai_batch,
        wait_for_openai_batch,
        download_openai_batch_results,
    )
    from services.scoring_service import compute_overall_score

    db = SessionLocal()
    try:
        api_key = settings.get_judge_api_key()
        model = settings.JUDGE_MODEL
        base_url = settings.OPENAI_BASE_URL

        outputs = db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()
        if not outputs:
            print(f"[Judge batch] No outputs for run {run_id}")
            return

        # Build batch lines
        lines = []
        # Track which outputs have which tasks
        output_map = {o.id: o for o in outputs}
        for output in outputs:
            item = db.query(DatasetItem).filter(DatasetItem.id == output.dataset_item_id).first()
            article = db.query(Article).filter(Article.id == output.article_id).first()
            if not item or not article:
                continue

            # Summary judge request
            if output.summary_output and item.summary_reference:
                lines.append(build_openai_batch_line(
                    custom_id=f"{output.id}__summary",
                    model=model,
                    system_prompt=SUMMARY_JUDGE_SYSTEM,
                    user_prompt=SUMMARY_JUDGE_USER.format(
                        article_body=article.body,
                        summary_reference=item.summary_reference,
                        summary_output=output.summary_output,
                    ),
                    json_mode=True,
                ))

            # Translation judge request
            if output.translation_output and item.translation_reference:
                lines.append(build_openai_batch_line(
                    custom_id=f"{output.id}__translation",
                    model=model,
                    system_prompt=TRANSLATION_JUDGE_SYSTEM,
                    user_prompt=TRANSLATION_JUDGE_USER.format(
                        english_source=item.translation_input,
                        translation_reference=item.translation_reference,
                        translation_output=output.translation_output,
                    ),
                    json_mode=True,
                ))

        if not lines:
            print(f"[Judge batch] Nothing to judge for run {run_id}")
            return

        print(f"[Judge batch] Submitting {len(lines)} judge requests for run {run_id}")
        batch_id = submit_openai_batch(api_key=api_key, lines=lines, base_url=base_url)
        print(f"[Judge batch] Batch ID: {batch_id}")

        def progress(status):
            c = status.get("request_counts", {})
            print(f"[Judge batch] status={status['status']} "
                  f"completed={c.get('completed', 0)}/{c.get('total', 0)} "
                  f"failed={c.get('failed', 0)}")

        wait_for_openai_batch(
            api_key=api_key, batch_id=batch_id, base_url=base_url,
            poll_interval=poll_interval, progress_callback=progress,
        )

        results = download_openai_batch_results(
            api_key=api_key, batch_id=batch_id, base_url=base_url,
        )
        print(f"[Judge batch] Got {len(results)} results")

        # Apply results
        from services.scoring_service import (
            compute_summary_score_from_rubric,
            compute_translation_score_from_rubric,
        )
        for cid, res in results.items():
            if "__" not in cid or res.get("status") != "ok":
                continue
            output_id, task = cid.rsplit("__", 1)
            output = output_map.get(output_id)
            if not output:
                continue
            try:
                rubric = parse_json_response(res["text"])
                if task == "summary":
                    output.judge_summary_rubric = rubric
                    output.summary_score = compute_summary_score_from_rubric(rubric)
                elif task == "translation":
                    output.judge_translation_rubric = rubric
                    output.translation_score = compute_translation_score_from_rubric(rubric)
            except Exception as e:
                print(f"[Judge batch] Failed to parse {cid}: {e}")

        # Recompute overall scores for all outputs
        for output in outputs:
            output.overall_score = compute_overall_score(
                output.ner_score or 0,
                output.nli_score or 0,
                output.summary_score or 0,
                output.translation_score or 0,
            )
            output.status = OutputStatus.SCORED
        db.commit()
        print(f"[Judge batch] Run {run_id} fully judged")

    finally:
        db.close()
