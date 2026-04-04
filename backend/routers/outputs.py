from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ModelOutput
from schemas import ModelOutputOut

router = APIRouter()


@router.get("/{run_id}", response_model=list[ModelOutputOut])
def list_outputs(run_id: str, db: Session = Depends(get_db)):
    return db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()


@router.get("/{run_id}/{article_id}", response_model=ModelOutputOut)
def get_output(run_id: str, article_id: str, db: Session = Depends(get_db)):
    output = (
        db.query(ModelOutput)
        .filter(ModelOutput.run_id == run_id, ModelOutput.article_id == article_id)
        .first()
    )
    if not output:
        raise HTTPException(404, "Output not found")
    return output
