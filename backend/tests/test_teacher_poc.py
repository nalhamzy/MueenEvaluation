"""POC test: generate dataset for 3 articles using real LLM calls.
Run with: py -m pytest backend/tests/test_teacher_poc.py -v -s
"""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Article, DatasetItem, ArticleStatus
from services.teacher_service import generate_for_article
from config import settings


# Use a dedicated test DB
engine = create_engine("sqlite:///./test_teacher.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)


def setup_module():
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    try:
        if os.path.exists("./test_teacher.db"):
            os.remove("./test_teacher.db")
    except PermissionError:
        pass  # Windows file lock; cleaned up on next run


def _load_sample_articles(db, count=3):
    """Load first N articles from the real JSON dataset."""
    json_path = os.path.join(os.path.dirname(__file__), "..", "..", "aljazeera_arabic_news_dataset_100_articles.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    articles = []
    for row in data[:count]:
        art_id = f"ART_{row['id']:03d}"
        existing = db.query(Article).filter(Article.id == art_id).first()
        if existing:
            articles.append(existing)
            continue
        article = Article(
            id=art_id,
            title=row["title"],
            body=row["body"],
            source=row.get("source", ""),
            status=ArticleStatus.PENDING,
        )
        db.add(article)
        articles.append(article)
    db.commit()
    return articles


def test_generate_3_articles():
    """Generate dataset items for 3 articles and verify structure."""
    db = Session()
    try:
        api_key = settings.get_teacher_api_key()
        assert api_key, "No API key configured - set OPENAI_API_KEY in .env"

        articles = _load_sample_articles(db, count=3)
        assert len(articles) == 3

        for article in articles:
            if article.status == ArticleStatus.READY:
                print(f"\n  SKIP {article.id} (already generated)")
                continue

            print(f"\n  Generating dataset for {article.id}...")
            item = generate_for_article(article, db)

            # Verify NER
            assert item.ner_reference is not None
            assert "PERSON" in item.ner_reference
            assert "LOCATION" in item.ner_reference
            assert "ORGANIZATION" in item.ner_reference
            assert "MISC" in item.ner_reference
            print(f"    NER: {len(item.ner_reference.get('PERSON', []))} persons, "
                  f"{len(item.ner_reference.get('LOCATION', []))} locations, "
                  f"{len(item.ner_reference.get('ORGANIZATION', []))} orgs")

            # Verify Summary
            assert item.summary_reference is not None
            assert len(item.summary_reference) > 20
            print(f"    Summary: {len(item.summary_reference)} chars")

            # Verify NLI
            assert item.nli_claims is not None
            assert len(item.nli_claims) >= 3
            labels = [c["label"] for c in item.nli_claims]
            assert "SUPPORTED" in labels
            assert "REFUTED" in labels
            print(f"    NLI: {len(item.nli_claims)} claims - {labels}")

            # Verify Coreference
            assert item.coref_reference is not None
            assert isinstance(item.coref_reference, list)
            for span_item in item.coref_reference:
                assert "span" in span_item
                assert "referent" in span_item
                assert "paragraph" in span_item
            print(f"    Coref: {len(item.coref_reference)} spans")

            # Verify article status
            assert article.status == ArticleStatus.READY
            print(f"    OK {article.id} complete")

        # Verify all items persisted
        count = db.query(DatasetItem).count()
        assert count == 3
        print(f"\n  Total DatasetItems in DB: {count}")

    finally:
        db.close()
