"""Tests for the generate-selected endpoint and article-id-based generation."""

import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app
from models import Article, ArticleStatus

TEST_DATABASE_URL = "sqlite:///./test_generate_selected.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


_original_overrides: dict = {}


def setup_module():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    # Save existing overrides (e.g. from conftest.py) and install our own
    global _original_overrides
    _original_overrides = dict(app.dependency_overrides)
    app.dependency_overrides[get_db] = override_get_db


def teardown_module():
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()
    # Restore the overrides that were active before this module ran
    app.dependency_overrides.clear()
    app.dependency_overrides.update(_original_overrides)
    try:
        os.remove("./test_generate_selected.db")
    except (FileNotFoundError, PermissionError):
        pass


def _seed_articles(count: int = 5):
    db = TestSession()
    try:
        # Clear existing
        db.query(Article).delete()
        db.commit()
        for i in range(count):
            db.add(Article(
                id=f"TEST_{i:03d}",
                title=f"Test article {i}",
                body=f"Body of article {i}. " * 20,
                source="test",
                status=ArticleStatus.READY,  # not PENDING
            ))
        db.commit()
    finally:
        db.close()


@patch("services.teacher_service.generate_dataset_task")
def test_generate_selected_picks_specific_articles(mock_task):
    """Endpoint should accept a list of article IDs and trigger generation."""
    _seed_articles(5)
    client = TestClient(app)

    resp = client.post(
        "/api/dataset/generate-selected",
        json={"article_ids": ["TEST_001", "TEST_003"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["selected"] == 2
    assert data["missing"] == []


@patch("services.teacher_service.generate_dataset_task")
def test_generate_selected_reports_missing(mock_task):
    """Missing article IDs should be reported, not cause an error."""
    _seed_articles(3)
    client = TestClient(app)

    resp = client.post(
        "/api/dataset/generate-selected",
        json={"article_ids": ["TEST_001", "NONEXISTENT_999"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["selected"] == 1
    assert "NONEXISTENT_999" in data["missing"]


def test_generate_selected_empty_list_rejected():
    """Empty article_ids list should return 400."""
    _seed_articles(3)
    client = TestClient(app)

    resp = client.post("/api/dataset/generate-selected", json={"article_ids": []})
    assert resp.status_code == 400


def test_generate_selected_all_missing_rejected():
    """If no articles match, should return 404."""
    _seed_articles(3)
    client = TestClient(app)

    resp = client.post(
        "/api/dataset/generate-selected",
        json={"article_ids": ["FAKE_001", "FAKE_002"]},
    )
    assert resp.status_code == 404


@patch("services.teacher_service.generate_dataset_task")
def test_generate_selected_resets_status_to_pending(mock_task):
    """Selected articles should have status reset to PENDING."""
    _seed_articles(3)
    client = TestClient(app)

    resp = client.post(
        "/api/dataset/generate-selected",
        json={"article_ids": ["TEST_001", "TEST_002"]},
    )
    assert resp.status_code == 200

    db = TestSession()
    try:
        a1 = db.query(Article).filter(Article.id == "TEST_001").first()
        a2 = db.query(Article).filter(Article.id == "TEST_002").first()
        a3 = db.query(Article).filter(Article.id == "TEST_000").first()
        assert a1.status == ArticleStatus.PENDING
        assert a2.status == ArticleStatus.PENDING
        # Untouched
        assert a3.status == ArticleStatus.READY
    finally:
        db.close()
