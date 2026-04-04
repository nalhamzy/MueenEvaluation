import threading
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ExecutiveSummary, EvaluationRun

router = APIRouter()


@router.get("/summary/{run_id}")
def get_summary(run_id: str, db: Session = Depends(get_db)):
    summary = (
        db.query(ExecutiveSummary)
        .filter(ExecutiveSummary.run_id == run_id)
        .order_by(ExecutiveSummary.generated_at.desc())
        .first()
    )
    if not summary:
        raise HTTPException(404, "No summary found for this run")
    return {"run_id": run_id, "content": summary.content, "generated_at": summary.generated_at}


@router.post("/generate/{run_id}")
def generate_summary(run_id: str, db: Session = Depends(get_db)):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(404, "Run not found")
    from services.report_service import generate_report_task
    t = threading.Thread(target=generate_report_task, args=(run_id,), daemon=True)
    t.start()
    return {"message": "Report generation started"}


@router.get("/comparison")
def comparison(db: Session = Depends(get_db)):
    """Cross-model comparison stats."""
    from services.report_service import get_comparison_stats
    return get_comparison_stats(db)


@router.get("/export/{run_id}")
def export_report(run_id: str, db: Session = Depends(get_db)):
    from services.report_service import export_run_report
    return export_run_report(run_id, db)
