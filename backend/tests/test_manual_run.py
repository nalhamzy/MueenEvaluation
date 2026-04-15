"""Tests for the manual run service (build_brief + create_manual_run)."""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from models import (
    Article, DatasetItem, ModelOutput, EvaluationRun,
    ArticleStatus, RunStatus, OutputStatus,
)
from services.manual_run_service import build_brief, create_manual_run

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)


def setup_module():
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def _seed_two_articles():
    db = Session()
    try:
        # Clear
        db.query(ModelOutput).delete()
        db.query(EvaluationRun).delete()
        db.query(DatasetItem).delete()
        db.query(Article).delete()
        db.commit()

        for i in range(2):
            aid = f"TEST_{i:03d}"
            art = Article(
                id=aid,
                title=f"Article {i}",
                body=f"Article body {i}. " * 10,
                source="test",
                status=ArticleStatus.READY,
            )
            db.add(art)
            db.commit()

            item = DatasetItem(
                article_id=aid,
                ner_input=art.body,
                ner_reference={
                    "PERSON": [f"Person{i}"],
                    "LOCATION": [f"City{i}"],
                    "ORGANIZATION": [],
                    "MISC": [],
                },
                summary_input=art.body,
                summary_reference=f"Reference summary {i}",
                nli_input=art.body,
                nli_claims=[
                    {"claim": f"claim a {i}", "label": "SUPPORTED"},
                    {"claim": f"claim b {i}", "label": "REFUTED"},
                    {"claim": f"claim c {i}", "label": "NOT_ENOUGH_INFO"},
                ],
                translation_input=f"English source {i} for translation.",
                translation_reference=f"الترجمة المرجعية {i}",
                generated_at=datetime.utcnow(),
                teacher_model="claude-opus-4-6",
            )
            db.add(item)
        db.commit()
    finally:
        db.close()


# --- build_brief tests ---

def test_brief_contains_articles_and_claims():
    _seed_two_articles()
    db = Session()
    try:
        brief = build_brief(["TEST_000", "TEST_001"], db)
        assert "TEST_000" in brief
        assert "TEST_001" in brief
        # Article body should appear
        assert "Article body 0" in brief
        # NLI claims should appear
        assert "claim a 0" in brief
        assert "claim b 0" in brief
        assert "claim c 0" in brief
        # Translation source should appear
        assert "English source 0 for translation" in brief
        # Should mention all 4 tasks
        assert "NER" in brief
        assert "SUMMARY" in brief.upper() or "Summary" in brief
        assert "NLI" in brief
        assert "TRANSLATION" in brief.upper() or "Translation" in brief
    finally:
        db.close()


def test_brief_preserves_requested_order():
    _seed_two_articles()
    db = Session()
    try:
        brief1 = build_brief(["TEST_000", "TEST_001"], db)
        brief2 = build_brief(["TEST_001", "TEST_000"], db)
        # In brief1, TEST_000 should appear before TEST_001
        assert brief1.index("TEST_000") < brief1.index("TEST_001")
        # In brief2, TEST_001 should appear before TEST_000
        assert brief2.index("TEST_001") < brief2.index("TEST_000")
    finally:
        db.close()


def test_brief_raises_for_unknown_articles():
    _seed_two_articles()
    db = Session()
    try:
        try:
            build_brief(["NONEXISTENT_999"], db)
            assert False, "should have raised ValueError"
        except ValueError:
            pass
    finally:
        db.close()


# --- create_manual_run tests ---

def test_create_manual_run_scores_outputs():
    _seed_two_articles()
    db = Session()
    try:
        payload = {
            "model_name": "test-model-via-cursor",
            "outputs": [
                {
                    "article_id": "TEST_000",
                    "ner_output": {
                        "PERSON": ["Person0"],
                        "LOCATION": ["City0"],
                        "ORGANIZATION": [],
                        "MISC": [],
                    },
                    "summary_output": "ملخص تجريبي",
                    "nli_output": [
                        {"claim": "claim a 0", "label": "SUPPORTED"},
                        {"claim": "claim b 0", "label": "REFUTED"},
                        {"claim": "claim c 0", "label": "NOT_ENOUGH_INFO"},
                    ],
                    "translation_output": "ترجمة تجريبية",
                },
            ],
        }
        result = create_manual_run(payload, db)
        assert result["scored_count"] == 1
        assert result["missing"] == []
        assert result["errors"] == []
        run_id = result["run_id"]

        # Verify a run was created and the output was scored
        run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
        assert run is not None
        assert run.status == RunStatus.COMPLETED
        assert run.processed_count == 1

        outputs = db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()
        assert len(outputs) == 1
        out = outputs[0]
        assert out.ner_score is not None
        assert out.nli_score is not None
        # NER perfect match → 10
        assert out.ner_score == 10.0
        # NLI all 3 correct → 10
        assert out.nli_score == 10.0
        # Summary/Translation are 0 (no judge run yet)
        assert out.summary_score == 0
        assert out.translation_score == 0
        # Overall = 10 * 0.30 + 10 * 0.20 + 0 * 0.25 + 0 * 0.25 = 5.0
        assert out.overall_score == 5.0
    finally:
        db.close()


def test_create_manual_run_reports_missing():
    _seed_two_articles()
    db = Session()
    try:
        payload = {
            "model_name": "test-model",
            "outputs": [
                {
                    "article_id": "TEST_000",
                    "ner_output": {"PERSON": [], "LOCATION": [], "ORGANIZATION": [], "MISC": []},
                    "summary_output": "x",
                    "nli_output": [],
                    "translation_output": "x",
                },
                {
                    "article_id": "FAKE_999",
                    "ner_output": {"PERSON": [], "LOCATION": [], "ORGANIZATION": [], "MISC": []},
                    "summary_output": "x",
                    "nli_output": [],
                    "translation_output": "x",
                },
            ],
        }
        result = create_manual_run(payload, db)
        assert result["scored_count"] == 1
        assert "FAKE_999" in result["missing"]
    finally:
        db.close()


def test_create_manual_run_rejects_empty():
    db = Session()
    try:
        try:
            create_manual_run({"model_name": "x", "outputs": []}, db)
            assert False, "should have raised"
        except ValueError:
            pass
    finally:
        db.close()
