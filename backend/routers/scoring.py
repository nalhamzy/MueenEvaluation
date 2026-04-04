import threading
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ModelOutput, DatasetItem
from schemas import ManualScoreRequest, ScoreBreakdown

router = APIRouter()


@router.post("/score-output", response_model=ScoreBreakdown)
def score_single_output(output_id: str, db: Session = Depends(get_db)):
    """Manually trigger scoring for one ModelOutput."""
    from services.scoring_service import score_output
    output = db.query(ModelOutput).filter(ModelOutput.id == output_id).first()
    if not output:
        raise HTTPException(404, "Output not found")
    result = score_output(output, db)
    return result


@router.post("/score-run/{run_id}")
def score_run(run_id: str, db: Session = Depends(get_db)):
    """Trigger deterministic scoring for entire run."""
    from services.scoring_service import score_run_task
    t = threading.Thread(target=score_run_task, args=(run_id,), daemon=True)
    t.start()
    return {"message": "Deterministic scoring started"}


@router.post("/judge-run/{run_id}")
def judge_run(run_id: str, db: Session = Depends(get_db)):
    """Trigger LLM judge scoring for entire run (summary)."""
    from services.judge_service import judge_run_task
    t = threading.Thread(target=judge_run_task, args=(run_id,), daemon=True)
    t.start()
    return {"message": "LLM judge scoring started"}


@router.post("/judge/{output_id}")
def judge_single_output(output_id: str, db: Session = Depends(get_db)):
    """Re-run LLM judge on one output."""
    from services.judge_service import judge_output
    output = db.query(ModelOutput).filter(ModelOutput.id == output_id).first()
    if not output:
        raise HTTPException(404, "Output not found")
    judge_output(output, db)
    return {"message": "Judge scoring complete", "overall_score": output.overall_score}


@router.post("/score-manual", response_model=ScoreBreakdown)
def score_manual(req: ManualScoreRequest, db: Session = Depends(get_db)):
    """Score a pasted LLM output against a specific article's DatasetItem."""
    from services.scoring_service import score_manual
    item = db.query(DatasetItem).filter(DatasetItem.article_id == req.article_id).first()
    if not item:
        raise HTTPException(404, "Dataset item not found for this article")
    return score_manual(item, req.task, req.model_output, db)
