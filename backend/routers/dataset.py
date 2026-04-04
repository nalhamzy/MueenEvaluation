import threading
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import DatasetItem, Article, ArticleStatus
from schemas import DatasetItemOut, DatasetStatsOut

router = APIRouter()


@router.post("/generate")
def generate_dataset(
    limit: int | None = None,
    db: Session = Depends(get_db),
):
    """Trigger Teacher LLM generation for PENDING articles. Optional limit param."""
    from services.teacher_service import generate_dataset_task

    pending = db.query(Article).filter(Article.status == ArticleStatus.PENDING).count()
    if pending == 0:
        return {"message": "No pending articles to process"}

    count = min(pending, limit) if limit else pending
    t = threading.Thread(target=generate_dataset_task, args=(limit,), daemon=True)
    t.start()
    return {"message": f"Dataset generation started for {count} articles"}


@router.get("", response_model=list[DatasetItemOut])
def list_dataset_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(DatasetItem).offset(skip).limit(limit).all()


@router.get("/stats", response_model=DatasetStatsOut)
def dataset_stats(db: Session = Depends(get_db)):
    total = db.query(DatasetItem).count()
    completed = db.query(DatasetItem).filter(DatasetItem.generated_at.isnot(None)).count()
    return DatasetStatsOut(total_items=total, completed=completed, pending=total - completed)


@router.get("/{article_id}", response_model=DatasetItemOut)
def get_dataset_item(article_id: str, db: Session = Depends(get_db)):
    item = db.query(DatasetItem).filter(DatasetItem.article_id == article_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Dataset item not found")
    return item
