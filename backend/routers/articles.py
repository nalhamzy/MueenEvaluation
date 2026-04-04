from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Article, DatasetItem, ModelOutput
from schemas import ArticleOut, ArticleUploadResponse
from services.csv_service import ingest_json, ingest_csv

router = APIRouter()


@router.post("/upload", response_model=ArticleUploadResponse)
async def upload_articles(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    filename = file.filename or ""

    if filename.endswith(".json"):
        result = ingest_json(content, db)
    elif filename.endswith(".csv"):
        result = ingest_csv(content, db)
    else:
        # Try JSON first, fall back to CSV
        try:
            result = ingest_json(content, db)
        except Exception:
            result = ingest_csv(content, db)

    return ArticleUploadResponse(**result)


@router.get("/count")
def count_articles(db: Session = Depends(get_db)):
    total = db.query(Article).count()
    by_status = dict(
        db.query(Article.status, func.count(Article.id))
        .group_by(Article.status)
        .all()
    )
    return {"total": total, "by_status": by_status}


@router.get("", response_model=list[ArticleOut])
def list_articles(
    skip: int = 0,
    limit: int = 100,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Article)
    if status:
        query = query.filter(Article.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{article_id}", response_model=ArticleOut)
def get_article(article_id: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.delete("/{article_id}")
def delete_article(article_id: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    # Delete related data first
    db.query(ModelOutput).filter(ModelOutput.article_id == article_id).delete()
    db.query(DatasetItem).filter(DatasetItem.article_id == article_id).delete()
    db.delete(article)
    db.commit()
    return {"message": f"Article {article_id} deleted"}


@router.delete("")
def delete_all_articles(confirm: bool = Query(False), db: Session = Depends(get_db)):
    """Delete all articles. Requires confirm=true query param."""
    if not confirm:
        raise HTTPException(400, "Pass ?confirm=true to delete all articles")
    db.query(ModelOutput).delete()
    db.query(DatasetItem).delete()
    db.query(Article).delete()
    db.commit()
    return {"message": "All articles deleted"}


@router.post("/reset-status")
def reset_error_articles(db: Session = Depends(get_db)):
    """Reset ERROR articles back to PENDING so they can be re-processed."""
    from models import ArticleStatus
    count = (
        db.query(Article)
        .filter(Article.status == ArticleStatus.ERROR)
        .update({Article.status: ArticleStatus.PENDING})
    )
    db.commit()
    return {"message": f"Reset {count} articles from ERROR to PENDING"}
