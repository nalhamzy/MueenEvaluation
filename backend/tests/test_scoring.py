"""Tests for deterministic scoring (NER, NLI) and rubric-based (Summary, Translation)."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.scoring_service import (
    normalize_arabic,
    compute_ner_score,
    compute_nli_score,
    compute_summary_score_from_rubric,
    compute_overall_score,
)


# --- Arabic normalization tests ---

def test_normalize_removes_diacritics():
    assert normalize_arabic("مُحَمَّد") == "محمد"


def test_normalize_alef_variants():
    assert normalize_arabic("إيران") == normalize_arabic("ايران")
    assert normalize_arabic("أحمد") == normalize_arabic("احمد")


def test_normalize_removes_al():
    assert normalize_arabic("القاهرة") == "قاهرة"


def test_normalize_strips_punctuation():
    assert normalize_arabic("القاهرة،") == "قاهرة"


# --- NER Scoring tests ---

def test_ner_perfect_score():
    reference = {
        "PERSON": ["محمد أحمد"],
        "LOCATION": ["القاهرة"],
        "ORGANIZATION": ["الأمم المتحدة"],
        "MISC": [],
    }
    predicted = {
        "PERSON": ["محمد أحمد"],
        "LOCATION": ["القاهرة"],
        "ORGANIZATION": ["الأمم المتحدة"],
        "MISC": [],
    }
    body = "محمد أحمد في القاهرة يعمل في الأمم المتحدة"
    result = compute_ner_score(predicted, reference, body)
    assert result["score"] == 10.0


def test_ner_zero_score():
    reference = {
        "PERSON": ["محمد"],
        "LOCATION": ["القاهرة"],
        "ORGANIZATION": [],
        "MISC": [],
    }
    predicted = {
        "PERSON": [],
        "LOCATION": [],
        "ORGANIZATION": [],
        "MISC": [],
    }
    result = compute_ner_score(predicted, reference, "محمد في القاهرة")
    # Empty predictions against non-empty references = 0 recall, but empty categories score 1.0
    # PERSON: 0 TP, 0 FP, 1 FN -> P=1.0, R=0.0, F1=0.0
    # LOCATION: 0 TP, 0 FP, 1 FN -> P=1.0, R=0.0, F1=0.0
    # ORG: both empty -> P=1.0, R=1.0, F1=1.0 (weight 0.25)
    # MISC: both empty -> P=1.0, R=1.0, F1=1.0 (weight 0.15)
    # Score = (0*0.35 + 0*0.25 + 1*0.25 + 1*0.15) * 10 = 4.0
    assert result["score"] == 4.0


def test_ner_partial_score():
    reference = {
        "PERSON": ["محمد", "أحمد"],
        "LOCATION": ["القاهرة"],
        "ORGANIZATION": [],
        "MISC": [],
    }
    predicted = {
        "PERSON": ["محمد"],
        "LOCATION": ["القاهرة"],
        "ORGANIZATION": [],
        "MISC": [],
    }
    body = "محمد وأحمد في القاهرة"
    result = compute_ner_score(predicted, reference, body)
    assert 0 < result["score"] < 10


def test_ner_hallucination_penalty():
    reference = {
        "PERSON": ["محمد"],
        "LOCATION": [],
        "ORGANIZATION": [],
        "MISC": [],
    }
    predicted = {
        "PERSON": ["محمد", "شخص_وهمي"],
        "LOCATION": [],
        "ORGANIZATION": [],
        "MISC": [],
    }
    body = "محمد في القاهرة"
    result = compute_ner_score(predicted, reference, body)
    assert result["hallucination_count"] >= 1
    assert result["penalty"] > 0


# --- NLI Scoring tests ---

def test_nli_perfect_score():
    reference = [
        {"claim": "ادعاء 1", "label": "SUPPORTED"},
        {"claim": "ادعاء 2", "label": "SUPPORTED"},
        {"claim": "ادعاء 3", "label": "REFUTED"},
        {"claim": "ادعاء 4", "label": "NOT_ENOUGH_INFO"},
    ]
    predicted = [
        {"claim": "ادعاء 1", "label": "SUPPORTED"},
        {"claim": "ادعاء 2", "label": "SUPPORTED"},
        {"claim": "ادعاء 3", "label": "REFUTED"},
        {"claim": "ادعاء 4", "label": "NOT_ENOUGH_INFO"},
    ]
    result = compute_nli_score(predicted, reference)
    assert result["score"] == 10.0


def test_nli_zero_score():
    reference = [
        {"claim": "ادعاء 1", "label": "SUPPORTED"},
        {"claim": "ادعاء 2", "label": "REFUTED"},
    ]
    predicted = [
        {"claim": "ادعاء 1", "label": "REFUTED"},
        {"claim": "ادعاء 2", "label": "SUPPORTED"},
    ]
    result = compute_nli_score(predicted, reference)
    assert result["score"] == 0.0


def test_nli_partial_score():
    reference = [
        {"claim": "ادعاء 1", "label": "SUPPORTED"},
        {"claim": "ادعاء 2", "label": "SUPPORTED"},
        {"claim": "ادعاء 3", "label": "REFUTED"},
        {"claim": "ادعاء 4", "label": "NOT_ENOUGH_INFO"},
    ]
    predicted = [
        {"claim": "ادعاء 1", "label": "SUPPORTED"},
        {"claim": "ادعاء 2", "label": "REFUTED"},  # wrong
        {"claim": "ادعاء 3", "label": "REFUTED"},
        {"claim": "ادعاء 4", "label": "SUPPORTED"},  # wrong
    ]
    result = compute_nli_score(predicted, reference)
    assert 0 < result["score"] < 10


def test_nli_weighted_harder_labels():
    """NOT_ENOUGH_INFO correct should give more weight than SUPPORTED correct."""
    ref = [
        {"claim": "c1", "label": "SUPPORTED"},
        {"claim": "c2", "label": "NOT_ENOUGH_INFO"},
    ]
    # Only SUPPORTED correct
    pred1 = [
        {"claim": "c1", "label": "SUPPORTED"},
        {"claim": "c2", "label": "SUPPORTED"},
    ]
    # Only NOT_ENOUGH_INFO correct
    pred2 = [
        {"claim": "c1", "label": "REFUTED"},
        {"claim": "c2", "label": "NOT_ENOUGH_INFO"},
    ]
    r1 = compute_nli_score(pred1, ref)
    r2 = compute_nli_score(pred2, ref)
    assert r2["score"] > r1["score"]


# --- Summary rubric scoring ---

def test_summary_perfect_rubric():
    rubric = {
        "factual_accuracy": 3,
        "coverage": 3,
        "no_added_inference": 2,
        "register_fluency": 2,
        "verbatim_penalty": 0,
    }
    score = compute_summary_score_from_rubric(rubric)
    assert score == 10.0


def test_summary_with_verbatim_penalty():
    rubric = {
        "factual_accuracy": 3,
        "coverage": 3,
        "no_added_inference": 2,
        "register_fluency": 2,
        "verbatim_penalty": 1,
    }
    score = compute_summary_score_from_rubric(rubric)
    assert score == 9.0


# --- Overall score ---

def test_overall_score_weights():
    # Weights: ner=0.30 + nli=0.20 + summary=0.25 + translation=0.25 = 1.0
    assert compute_overall_score(10, 10, 10, 10) == 10.0
    assert compute_overall_score(0, 0, 0, 0) == 0.0

    assert compute_overall_score(10, 0, 0, 0) == 3.0   # ner = 0.30
    assert compute_overall_score(0, 10, 0, 0) == 2.0   # nli = 0.20
    assert compute_overall_score(0, 0, 10, 0) == 2.5   # summary = 0.25
    assert compute_overall_score(0, 0, 0, 10) == 2.5   # translation = 0.25
