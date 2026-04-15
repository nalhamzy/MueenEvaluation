"""Student LLM service - runs evaluation prompts against dataset items."""

from datetime import datetime
from sqlalchemy.orm import Session
from models import (
    EvaluationRun, DatasetItem, ModelOutput, RunStatus, OutputStatus,
)
from services.llm_client import call_llm, parse_json_response, unwrap_json_list
from services.teacher_service import (
    NER_SYSTEM, NER_USER, SUMMARY_SYSTEM, SUMMARY_USER,
    NLI_SYSTEM, NLI_USER,
    TRANSLATION_SYSTEM,
)
from config import settings


def evaluate_single_item(
    item: DatasetItem,
    run: EvaluationRun,
    api_key: str,
    db: Session,
) -> ModelOutput:
    """Run all 5 tasks for one dataset item with a student model."""
    model = run.model_name
    base_url = run.api_base_url or settings.OPENAI_BASE_URL

    output = (
        db.query(ModelOutput)
        .filter(ModelOutput.run_id == run.id, ModelOutput.dataset_item_id == item.id)
        .first()
    )
    if not output:
        output = ModelOutput(
            run_id=run.id,
            dataset_item_id=item.id,
            article_id=item.article_id,
            status=OutputStatus.RUNNING,
        )
        db.add(output)
        db.commit()
    else:
        output.status = OutputStatus.RUNNING
        db.commit()

    try:
        # 1. NER
        ner_raw = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=NER_SYSTEM,
            user_prompt=NER_USER.format(article_body=item.ner_input),
            json_mode=True, db=db, task_type="student_ner",
        )
        try:
            output.ner_output = parse_json_response(ner_raw)
        except Exception:
            output.ner_output = {"PERSON": [], "LOCATION": [], "ORGANIZATION": [], "MISC": []}

        # 2. Summary
        output.summary_output = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=SUMMARY_SYSTEM,
            user_prompt=SUMMARY_USER.format(article_body=item.summary_input),
            db=db, task_type="student_summary",
        ).strip()

        # 3. NLI - send claims for labeling
        nli_claims_text = "\n".join(
            f'{i+1}. {c["claim"]}' for i, c in enumerate(item.nli_claims or [])
        )
        nli_system = (
            "You are an expert Arabic fact-checking annotator. "
            "Output valid JSON only. No markdown. No preamble."
        )
        nli_user = (
            f"Given the following Arabic news article and claims, label each claim as "
            f'"SUPPORTED", "REFUTED", or "NOT_ENOUGH_INFO" based solely on the article.\n\n'
            f"Article:\n{item.nli_input}\n\n"
            f"Claims:\n{nli_claims_text}\n\n"
            f"Return a JSON array: "
            f'[{{"claim": "...", "label": "SUPPORTED|REFUTED|NOT_ENOUGH_INFO"}}, ...]'
        )
        nli_raw = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=nli_system, user_prompt=nli_user,
            json_mode=True, db=db, task_type="student_nli",
        )
        try:
            nli_parsed = parse_json_response(nli_raw)
            output.nli_output = unwrap_json_list(nli_parsed)
        except Exception:
            output.nli_output = []

        # 4. Translation (Eng→Arabic)
        translation_system = (
            "You are an expert English-to-Arabic translator. Write only in formal "
            "Modern Standard Arabic (فصحى). No dialect. Output the translation only."
        )
        translation_user = (
            f"Translate the following English text to formal Arabic (فصحى).\n\n"
            f"English:\n{item.translation_input}\n\n"
            f"Rules:\n"
            f"1. Translate faithfully — do not add or omit information.\n"
            f"2. Use formal MSA register throughout.\n"
            f"3. Output only the Arabic translation, nothing else."
        )
        output.translation_output = call_llm(
            api_key=api_key, model=model, base_url=base_url,
            system_prompt=translation_system,
            user_prompt=translation_user,
            db=db, task_type="student_translation",
        ).strip()

        output.status = OutputStatus.PENDING  # pending scoring
        output.processed_at = datetime.utcnow()
        db.commit()
        return output

    except Exception as e:
        output.status = OutputStatus.ERROR
        output.error_message = str(e)[:500]
        db.commit()
        return output


def run_evaluation_task(
    run_id: str,
    api_key: str | None = None,
    limit: int | None = None,
    article_ids: list[str] | None = None,
):
    """Background task to run full evaluation for a run.

    If article_ids is provided, only those specific articles are evaluated.
    Otherwise, all dataset items with generated_at NOT NULL are evaluated
    (optionally limited by `limit`).
    """
    from database import SessionLocal
    db = SessionLocal()
    try:
        run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
        if not run:
            return

        run.status = RunStatus.RUNNING
        run.started_at = datetime.utcnow()
        db.commit()

        api_key = api_key or settings.get_student_api_key()
        query = db.query(DatasetItem).filter(DatasetItem.generated_at.isnot(None))
        if article_ids:
            query = query.filter(DatasetItem.article_id.in_(article_ids))
        if limit:
            query = query.limit(limit)
        items = query.all()

        run.total_articles = len(items)
        run.processed_count = 0
        db.commit()

        for item in items:
            # Check if run was cancelled
            db.refresh(run)
            if run.status == RunStatus.FAILED:
                break

            try:
                evaluate_single_item(item, run, api_key, db)
                run.processed_count += 1
                db.commit()
                print(f"[Student] {run.model_name}: {item.article_id} done "
                      f"({run.processed_count}/{run.total_articles})")
            except Exception as e:
                print(f"[Student] ERROR on {item.article_id}: {e}")
                run.processed_count += 1
                db.commit()

        # Score all outputs
        from services.scoring_service import score_run_task
        score_run_task(run_id)

        # Update run status
        db.refresh(run)
        if run.status != RunStatus.FAILED:
            run.status = RunStatus.COMPLETED
            run.completed_at = datetime.utcnow()
            db.commit()

    except Exception as e:
        run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
        if run:
            run.status = RunStatus.FAILED
            run.error_message = str(e)[:500]
            db.commit()
    finally:
        db.close()
