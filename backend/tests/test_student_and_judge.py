"""Tests for student evaluation and judge scoring flows.
Unit tests use mocked LLM calls to test the pipeline logic.
"""

import sys
import os
import json
from unittest.mock import patch, MagicMock
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import (
    Article, DatasetItem, EvaluationRun, ModelOutput,
    ArticleStatus, RunStatus, OutputStatus,
)
from services.scoring_service import (
    compute_ner_score, compute_nli_score,
    compute_summary_score_from_rubric,
    compute_translation_score_from_rubric,
    compute_overall_score,
)

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)


def setup_module():
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def _seed_data(db):
    """Insert an article, dataset item, run, and output for testing."""
    art = Article(
        id="ART_TEST",
        title="Test Article",
        body="This is a test article body.",
        status=ArticleStatus.READY,
    )
    db.merge(art)

    item = DatasetItem(
        id="ds_test_001",
        article_id="ART_TEST",
        ner_input="Test article body.",
        ner_reference={
            "PERSON": ["Ahmed"],
            "LOCATION": ["Cairo"],
            "ORGANIZATION": ["UN"],
            "MISC": [],
        },
        summary_input="Test article body.",
        summary_reference="A concise test summary.",
        nli_input="Test article body.",
        nli_claims=[
            {"claim": "Claim 1", "label": "SUPPORTED"},
            {"claim": "Claim 2", "label": "SUPPORTED"},
            {"claim": "Claim 3", "label": "REFUTED"},
            {"claim": "Claim 4", "label": "NOT_ENOUGH_INFO"},
        ],
        translation_input="This is a test English sentence about events in the region.",
        translation_reference="هذه جملة اختبارية عن الأحداث في المنطقة.",
        generated_at=datetime.utcnow(),
        teacher_model="gpt-4o",
    )
    db.merge(item)

    run = EvaluationRun(
        id="run_test_001",
        model_name="gpt-4o-mini",
        status=RunStatus.RUNNING,
        total_articles=1,
    )
    db.merge(run)
    db.commit()
    return art, item, run


# --- Student output scoring tests ---

def test_score_model_output_ner():
    """Test that a student NER output gets scored correctly."""
    db = Session()
    art, item, run = _seed_data(db)

    output = ModelOutput(
        id="out_ner_test",
        run_id=run.id,
        dataset_item_id=item.id,
        article_id=art.id,
        ner_output={
            "PERSON": ["Ahmed"],
            "LOCATION": ["Cairo"],
            "ORGANIZATION": [],
            "MISC": [],
        },
        status=OutputStatus.PENDING,
    )
    db.merge(output)
    db.commit()

    # Compute NER score
    result = compute_ner_score(output.ner_output, item.ner_reference, art.body)
    # PERSON: perfect match (F1=1.0, weight=0.35)
    # LOCATION: perfect match (F1=1.0, weight=0.25)
    # ORG: ref has UN, pred has none (F1=0.0, weight=0.25)
    # MISC: both empty (F1=1.0, weight=0.15)
    assert result["score"] > 0
    assert result["category_scores"]["PERSON"]["f1"] == 1.0
    assert result["category_scores"]["LOCATION"]["f1"] == 1.0
    assert result["category_scores"]["ORGANIZATION"]["f1"] == 0.0
    db.close()


def test_score_model_output_nli():
    """Test NLI scoring with partial correctness."""
    ref = [
        {"claim": "c1", "label": "SUPPORTED"},
        {"claim": "c2", "label": "SUPPORTED"},
        {"claim": "c3", "label": "REFUTED"},
        {"claim": "c4", "label": "NOT_ENOUGH_INFO"},
    ]
    pred = [
        {"claim": "c1", "label": "SUPPORTED"},
        {"claim": "c2", "label": "REFUTED"},       # wrong
        {"claim": "c3", "label": "REFUTED"},        # correct
        {"claim": "c4", "label": "NOT_ENOUGH_INFO"}, # correct
    ]
    result = compute_nli_score(pred, ref)
    # Correct: SUPPORTED(1.0) + REFUTED(1.2) + NOT_ENOUGH_INFO(1.5) = 3.7
    # Total:   1.0 + 1.0 + 1.2 + 1.5 = 4.7
    expected = 3.7 / 4.7 * 10
    assert abs(result["score"] - round(expected, 2)) < 0.1


def test_full_scoring_pipeline():
    """Test the full scoring pipeline: deterministic + rubric computation."""
    # Summary rubric
    rubric = {
        "factual_accuracy": 2,
        "coverage": 2,
        "no_added_inference": 1,
        "register_fluency": 1,
        "verbatim_penalty": 0,
    }
    summary_score = compute_summary_score_from_rubric(rubric)
    assert 0 < summary_score < 10

    # Translation rubric
    trans_rubric = {
        "faithfulness": 2,
        "fluency": 2,
        "terminology": 1,
        "register": 1,
    }
    trans_score = compute_translation_score_from_rubric(trans_rubric)
    assert 0 < trans_score < 10

    # Overall
    overall = compute_overall_score(7.5, 8.0, summary_score, trans_score)
    assert 0 < overall <= 10


def test_overall_score_boundary():
    """Verify boundary conditions for overall score.
    Weights: ner=0.30, nli=0.20, summary=0.25, translation=0.25
    """
    assert compute_overall_score(0, 0, 0, 0) == 0.0
    assert compute_overall_score(10, 10, 10, 10) == 10.0

    assert compute_overall_score(10, 0, 0, 0) == 3.0   # NER weight = 0.30
    assert compute_overall_score(0, 10, 0, 0) == 2.0   # NLI weight = 0.20
    assert compute_overall_score(0, 0, 10, 0) == 2.5   # Summary weight = 0.25
    assert compute_overall_score(0, 0, 0, 10) == 2.5   # Translation weight = 0.25


def test_model_output_lifecycle():
    """Test that a ModelOutput transitions through statuses correctly."""
    db = Session()
    _seed_data(db)

    output = ModelOutput(
        id="out_lifecycle",
        run_id="run_test_001",
        dataset_item_id="ds_test_001",
        article_id="ART_TEST",
        status=OutputStatus.PENDING,
    )
    db.merge(output)
    db.commit()

    assert output.status == OutputStatus.PENDING

    output.status = OutputStatus.RUNNING
    db.commit()
    assert output.status == OutputStatus.RUNNING

    output.ner_output = {"PERSON": [], "LOCATION": [], "ORGANIZATION": [], "MISC": []}
    output.ner_score = 5.0
    output.nli_output = []
    output.nli_score = 6.0
    output.summary_score = 7.0
    output.translation_score = 9.0
    output.overall_score = compute_overall_score(5.0, 6.0, 7.0, 9.0)
    output.status = OutputStatus.SCORED
    db.commit()

    assert output.status == OutputStatus.SCORED
    # ner*0.30 + nli*0.20 + summary*0.25 + translation*0.25
    assert output.overall_score == round(5.0*0.30 + 6.0*0.20 + 7.0*0.25 + 9.0*0.25, 2)
    db.close()


@patch("services.student_service.call_llm")
def test_evaluate_single_item_mocked(mock_llm):
    """Test evaluate_single_item with mocked LLM calls."""
    from services.student_service import evaluate_single_item

    mock_llm.side_effect = [
        '{"PERSON": ["Ahmed"], "LOCATION": [], "ORGANIZATION": [], "MISC": []}',  # NER
        "A student summary.",                                                       # Summary
        '[{"claim": "c1", "label": "SUPPORTED"}, {"claim": "c2", "label": "SUPPORTED"}, '
        '{"claim": "c3", "label": "REFUTED"}, {"claim": "c4", "label": "NOT_ENOUGH_INFO"}]',  # NLI
        "ترجمة تجريبية للنص الإنجليزي.",  # Translation
    ]

    db = Session()
    _seed_data(db)

    item = db.query(DatasetItem).filter(DatasetItem.id == "ds_test_001").first()
    run = db.query(EvaluationRun).filter(EvaluationRun.id == "run_test_001").first()

    output = evaluate_single_item(item, run, "fake-key", db)

    assert output is not None
    assert output.ner_output["PERSON"] == ["Ahmed"]
    assert output.summary_output == "A student summary."
    assert len(output.nli_output) == 4
    assert output.translation_output is not None
    assert output.status == OutputStatus.PENDING  # pending scoring
    assert mock_llm.call_count == 4
    db.close()
