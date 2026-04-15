"""Report service - executive summary generation and exports."""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import (
    EvaluationRun, ModelOutput, ExecutiveSummary, RunStatus, OutputStatus,
)
from services.llm_client import call_llm
from config import settings


REPORT_SYSTEM = (
    "You are a senior NLP research lead writing an evaluation report. "
    "Write in clear, professional English. Use markdown formatting."
)

REPORT_USER = """Generate an executive summary report for the following Arabic LLM evaluation run.

Model evaluated: {model_name}
Total articles: {total_articles}
Articles successfully scored: {scored_count}

Aggregate scores:
  NER:            {avg_ner:.2f} / 10
  NLI:            {avg_nli:.2f} / 10
  Summarization:  {avg_summary:.2f} / 10
  Translation:    {avg_translation:.2f} / 10
  Overall:        {avg_overall:.2f} / 10

Score distribution:
  Articles scoring > 8.0: {high_count}
  Articles scoring 5.0-8.0: {mid_count}
  Articles scoring < 5.0: {low_count}

Most common judge feedback themes (from rubric reasoning fields):
{top_failure_themes}

Top 3 worst-performing articles:
{worst_articles}

Write a report with these sections:
## Overall Performance
## Strengths
## Weaknesses
## Task-by-Task Analysis
## Recommendations for Improvement
## Conclusion

Be specific. Reference actual scores. Identify patterns."""


def _get_run_stats(run_id: str, db: Session) -> dict:
    """Gather all statistics needed for the report prompt."""
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    outputs = db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()
    scored = [o for o in outputs if o.status == OutputStatus.SCORED]

    if not scored:
        return None

    avg_ner = sum(o.ner_score or 0 for o in scored) / len(scored)
    avg_nli = sum(o.nli_score or 0 for o in scored) / len(scored)
    avg_summary = sum(o.summary_score or 0 for o in scored) / len(scored)
    avg_translation = sum(o.translation_score or 0 for o in scored) / len(scored)
    avg_overall = sum(o.overall_score or 0 for o in scored) / len(scored)

    high_count = sum(1 for o in scored if (o.overall_score or 0) > 8.0)
    mid_count = sum(1 for o in scored if 5.0 <= (o.overall_score or 0) <= 8.0)
    low_count = sum(1 for o in scored if (o.overall_score or 0) < 5.0)

    # Collect judge reasoning themes
    themes = []
    for o in scored:
        if o.judge_summary_rubric and "reasoning" in o.judge_summary_rubric:
            themes.append(o.judge_summary_rubric["reasoning"])
        if o.judge_translation_rubric and "reasoning" in o.judge_translation_rubric:
            themes.append(o.judge_translation_rubric["reasoning"])

    # Worst performing
    worst = sorted(scored, key=lambda o: o.overall_score or 0)[:3]
    worst_text = "\n".join(
        f"  - {o.article_id}: overall={o.overall_score:.1f} "
        f"(NER={o.ner_score:.1f}, NLI={o.nli_score:.1f}, "
        f"Summary={o.summary_score:.1f}, "
        f"Translation={o.translation_score:.1f})"
        for o in worst
    )

    return {
        "model_name": run.model_name,
        "total_articles": run.total_articles,
        "scored_count": len(scored),
        "avg_ner": avg_ner,
        "avg_nli": avg_nli,
        "avg_summary": avg_summary,
        "avg_translation": avg_translation,
        "avg_overall": avg_overall,
        "high_count": high_count,
        "mid_count": mid_count,
        "low_count": low_count,
        "top_failure_themes": "\n".join(themes[:10]) if themes else "(no judge feedback yet)",
        "worst_articles": worst_text or "(no data)",
    }


def generate_report_task(run_id: str):
    """Background task to generate executive summary for a run."""
    from database import SessionLocal
    db = SessionLocal()
    try:
        stats = _get_run_stats(run_id, db)
        if not stats:
            return

        api_key = settings.get_judge_api_key()
        content = call_llm(
            api_key=api_key,
            model=settings.JUDGE_MODEL,
            base_url=settings.OPENAI_BASE_URL,
            system_prompt=REPORT_SYSTEM,
            user_prompt=REPORT_USER.format(**stats),
            db=db,
            task_type="report_generation",
        )

        # Save or update
        existing = (
            db.query(ExecutiveSummary)
            .filter(ExecutiveSummary.run_id == run_id)
            .first()
        )
        if existing:
            existing.content = content.strip()
            existing.generated_at = datetime.utcnow()
        else:
            summary = ExecutiveSummary(
                run_id=run_id,
                content=content.strip(),
            )
            db.add(summary)
        db.commit()
        print(f"[Report] Generated executive summary for run {run_id}")

    except Exception as e:
        print(f"[Report] ERROR generating report: {e}")
    finally:
        db.close()


def get_comparison_stats(db: Session) -> dict:
    """Cross-model comparison statistics."""
    runs = db.query(EvaluationRun).filter(
        EvaluationRun.status == RunStatus.COMPLETED
    ).all()

    comparison = []
    for run in runs:
        avg_scores = (
            db.query(
                func.avg(ModelOutput.ner_score),
                func.avg(ModelOutput.nli_score),
                func.avg(ModelOutput.summary_score),
                func.avg(ModelOutput.translation_score),
                func.avg(ModelOutput.overall_score),
                func.count(ModelOutput.id),
            )
            .filter(ModelOutput.run_id == run.id, ModelOutput.status == OutputStatus.SCORED)
            .first()
        )
        comparison.append({
            "run_id": run.id,
            "model_name": run.model_name,
            "scored_count": avg_scores[5] or 0,
            "avg_ner": round(avg_scores[0] or 0, 2),
            "avg_nli": round(avg_scores[1] or 0, 2),
            "avg_summary": round(avg_scores[2] or 0, 2),
            "avg_translation": round(avg_scores[3] or 0, 2),
            "avg_overall": round(avg_scores[4] or 0, 2),
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        })

    return {"models": comparison}


def export_run_report(run_id: str, db: Session) -> dict:
    """Export full run report as JSON."""
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        return {"error": "Run not found"}

    outputs = db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()

    summary = (
        db.query(ExecutiveSummary)
        .filter(ExecutiveSummary.run_id == run_id)
        .order_by(ExecutiveSummary.generated_at.desc())
        .first()
    )

    return {
        "run": {
            "id": run.id,
            "model_name": run.model_name,
            "status": run.status.value if hasattr(run.status, "value") else run.status,
            "total_articles": run.total_articles,
            "processed_count": run.processed_count,
            "started_at": run.started_at.isoformat() if run.started_at else None,
            "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        },
        "outputs": [
            {
                "article_id": o.article_id,
                "ner_score": o.ner_score,
                "nli_score": o.nli_score,
                "summary_score": o.summary_score,
                "translation_score": o.translation_score,
                "overall_score": o.overall_score,
                "status": o.status.value if hasattr(o.status, "value") else o.status,
                "judge_summary_rubric": o.judge_summary_rubric,
                "judge_translation_rubric": o.judge_translation_rubric,
            }
            for o in outputs
        ],
        "executive_summary": summary.content if summary else None,
    }
