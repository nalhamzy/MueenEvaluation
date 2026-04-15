import threading
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import DatasetItem, Article, ArticleStatus
from schemas import DatasetItemOut, DatasetStatsOut

router = APIRouter()


class GenerateSelectedRequest(BaseModel):
    article_ids: list[str]


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


@router.post("/generate-selected")
def generate_selected(req: GenerateSelectedRequest, db: Session = Depends(get_db)):
    """Trigger Teacher LLM generation for a specific list of article IDs.
    Articles must exist; their status is reset to PENDING before generation.
    """
    from services.teacher_service import generate_dataset_task

    if not req.article_ids:
        raise HTTPException(400, "article_ids list is empty")

    found = db.query(Article).filter(Article.id.in_(req.article_ids)).all()
    found_ids = {a.id for a in found}
    missing = [aid for aid in req.article_ids if aid not in found_ids]

    if not found:
        raise HTTPException(404, "No matching articles found")

    # Reset their status so generate_dataset_task picks them up
    for a in found:
        if a.status != ArticleStatus.PENDING:
            a.status = ArticleStatus.PENDING
    db.commit()

    t = threading.Thread(
        target=generate_dataset_task,
        kwargs={"article_ids": req.article_ids},
        daemon=True,
    )
    t.start()

    return {
        "message": f"Generation started for {len(found)} articles",
        "selected": len(found),
        "missing": missing,
    }


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
