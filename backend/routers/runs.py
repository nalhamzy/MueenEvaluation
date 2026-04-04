from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import EvaluationRun, RunStatus, DatasetItem, ModelOutput, OutputStatus
from schemas import RunCreate, RunOut, ModelOutputOut
import threading
import json

router = APIRouter()


@router.post("", response_model=RunOut)
def create_run(req: RunCreate, db: Session = Depends(get_db)):
    total = db.query(DatasetItem).filter(DatasetItem.generated_at.isnot(None)).count()
    if total == 0:
        raise HTTPException(400, "No dataset items available. Generate dataset first.")

    # Resolve model from registry if no explicit API key/base_url provided
    from services.model_registry import get_model_by_id, get_api_key_for_model
    api_key = req.api_key
    base_url = req.base_url
    model_name = req.model_name

    registry_model = get_model_by_id(req.model_name)
    if registry_model:
        model_name = registry_model["model_id"]
        if not api_key:
            api_key, base_url = get_api_key_for_model(req.model_name)
        if not base_url:
            base_url = registry_model.get("base_url")

    effective_total = min(total, req.limit) if req.limit else total

    run = EvaluationRun(
        model_name=model_name,
        api_base_url=base_url,
        total_articles=effective_total,
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    # Run in a separate thread so it doesn't block the API
    from services.student_service import run_evaluation_task
    t = threading.Thread(target=run_evaluation_task, args=(run.id, api_key, req.limit), daemon=True)
    t.start()

    return run


@router.get("", response_model=list[RunOut])
def list_runs(db: Session = Depends(get_db)):
    return db.query(EvaluationRun).order_by(EvaluationRun.started_at.desc()).all()


@router.get("/{run_id}", response_model=RunOut)
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(404, "Run not found")
    return run


@router.get("/{run_id}/outputs", response_model=list[ModelOutputOut])
def get_run_outputs(run_id: str, db: Session = Depends(get_db)):
    """All outputs for a run with scores."""
    return db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()


@router.get("/{run_id}/scores")
def get_run_scores(run_id: str, db: Session = Depends(get_db)):
    """Aggregate score stats for a run."""
    outputs = (
        db.query(ModelOutput)
        .filter(ModelOutput.run_id == run_id, ModelOutput.status == OutputStatus.SCORED)
        .all()
    )
    if not outputs:
        return {"count": 0}

    return {
        "count": len(outputs),
        "avg_ner": round(sum(o.ner_score or 0 for o in outputs) / len(outputs), 2),
        "avg_nli": round(sum(o.nli_score or 0 for o in outputs) / len(outputs), 2),
        "avg_summary": round(sum(o.summary_score or 0 for o in outputs) / len(outputs), 2),
        "avg_coref": round(sum(o.coref_score or 0 for o in outputs) / len(outputs), 2),
        "avg_translation": round(sum(o.translation_score or 0 for o in outputs) / len(outputs), 2),
        "avg_overall": round(sum(o.overall_score or 0 for o in outputs) / len(outputs), 2),
        "scores": [
            {
                "article_id": o.article_id,
                "ner": o.ner_score,
                "nli": o.nli_score,
                "summary": o.summary_score,
                "coref": o.coref_score,
                "translation": o.translation_score,
                "overall": o.overall_score,
            }
            for o in outputs
        ],
    }


@router.delete("/{run_id}")
def cancel_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
    if not run:
        raise HTTPException(404, "Run not found")
    if run.status in (RunStatus.QUEUED, RunStatus.RUNNING):
        run.status = RunStatus.FAILED
        run.error_message = "Cancelled by user"
        db.commit()
    return {"message": "Run cancelled"}
