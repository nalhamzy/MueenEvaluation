"""Service for ingesting articles from CSV or JSON files."""

import csv
import json
import io
from datetime import datetime, date
from sqlalchemy.orm import Session
from models import Article, ArticleStatus


def parse_date(date_str: str | None) -> date | None:
    if not date_str:
        return None
    try:
        # Try ISO 8601 with time
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).date()
    except (ValueError, TypeError):
        pass
    try:
        # Try plain date
        return date.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


def ingest_json(file_content: bytes, db: Session) -> dict:
    """Parse JSON array of articles and insert into DB."""
    data = json.loads(file_content.decode("utf-8"))
    if not isinstance(data, list):
        raise ValueError("JSON must be an array of articles")
    return _insert_articles(data, db, source_format="json")


def ingest_csv(file_content: bytes, db: Session) -> dict:
    """Parse CSV of articles and insert into DB."""
    text = file_content.decode("utf-8-sig")  # handle BOM
    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)
    return _insert_articles(rows, db, source_format="csv")


def _insert_articles(rows: list[dict], db: Session, source_format: str) -> dict:
    inserted = 0
    skipped = 0
    errors = []

    for i, row in enumerate(rows):
        try:
            # Normalize field names between JSON and CSV formats
            article_id = str(row.get("article_id") or row.get("id") or f"ART_{i+1:03d}")
            article_id = f"ART_{article_id:>03}" if article_id.isdigit() else article_id

            title = row.get("title", "")
            body = row.get("body", "")
            source = row.get("source", "")
            date_val = parse_date(
                row.get("date") or row.get("date_published")
            )

            if not title or not body:
                errors.append(f"Row {i+1}: missing title or body")
                continue

            # Check for duplicate
            existing = db.query(Article).filter(Article.id == article_id).first()
            if existing:
                skipped += 1
                continue

            article = Article(
                id=article_id,
                title=title,
                body=body,
                source=source,
                date=date_val,
                status=ArticleStatus.PENDING,
            )
            db.add(article)
            inserted += 1

        except Exception as e:
            errors.append(f"Row {i+1}: {str(e)}")

    db.commit()

    return {
        "total": len(rows),
        "inserted": inserted,
        "skipped": skipped,
        "errors": errors,
    }
