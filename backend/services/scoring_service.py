"""Scoring service - deterministic (NER, NLI, coref) and LLM judge (summary)."""

import re
import json
from sqlalchemy.orm import Session
from models import ModelOutput, DatasetItem, Article, OutputStatus
from schemas import ScoreBreakdown


# --- Arabic normalization ---

def normalize_arabic(text: str) -> str:
    # Remove diacritics (tashkeel)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    # Normalize alef variants to bare alef
    text = re.sub(r'[إأآا]', 'ا', text)
    # Remove definite article ال
    text = re.sub(r'^ال', '', text.strip())
    # Remove trailing punctuation
    text = text.strip('.,،؛:؟!')
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text


# --- NER Scoring (Deterministic, 0-10) ---

NER_WEIGHTS = {
    "PERSON": 0.35,
    "LOCATION": 0.25,
    "ORGANIZATION": 0.25,
    "MISC": 0.15,
}


def compute_ner_score(predicted: dict, reference: dict, article_body: str) -> dict:
    """Compute NER F1 score per category, with hallucination penalty."""
    category_scores = {}
    hallucination_count = 0

    for category, weight in NER_WEIGHTS.items():
        ref_entities = {normalize_arabic(e) for e in reference.get(category, [])}
        pred_entities = {normalize_arabic(e) for e in predicted.get(category, [])}

        tp = len(pred_entities & ref_entities)
        fp = len(pred_entities) - tp
        fn = len(ref_entities) - tp

        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        # Check for hallucinated entities (in prediction but not in article body)
        normalized_body = normalize_arabic(article_body)
        for entity in pred_entities - ref_entities:
            if entity not in normalized_body:
                hallucination_count += 1

        category_scores[category] = {
            "f1": f1,
            "precision": precision,
            "recall": recall,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "weight": weight,
        }

    weighted_f1 = sum(
        category_scores[cat]["f1"] * NER_WEIGHTS[cat]
        for cat in NER_WEIGHTS
    )
    raw_score = weighted_f1 * 10

    # Hallucination penalty: -1.5 per hallucination, capped at -3.0
    penalty = min(hallucination_count * 1.5, 3.0)
    final_score = max(0, raw_score - penalty)

    return {
        "score": round(final_score, 2),
        "category_scores": category_scores,
        "hallucination_count": hallucination_count,
        "penalty": penalty,
        "raw_score": round(raw_score, 2),
    }


# --- NLI Scoring (Deterministic, 0-10) ---

NLI_LABEL_WEIGHTS = {
    "NOT_ENOUGH_INFO": 1.5,
    "REFUTED": 1.2,
    "SUPPORTED": 1.0,
}


def compute_nli_score(predicted: list[dict], reference: list[dict]) -> dict:
    """Compute NLI accuracy with per-label weights."""
    if not reference:
        return {"score": 0, "details": {"error": "No reference claims"}}

    total_weight = 0
    weighted_correct = 0
    per_claim = []

    for i, ref_claim in enumerate(reference):
        ref_label = ref_claim["label"]
        weight = NLI_LABEL_WEIGHTS.get(ref_label, 1.0)
        total_weight += weight

        pred_label = None
        if i < len(predicted):
            pred_label = predicted[i].get("label", "")

        correct = pred_label == ref_label
        if correct:
            weighted_correct += weight

        per_claim.append({
            "claim": ref_claim["claim"],
            "reference_label": ref_label,
            "predicted_label": pred_label,
            "correct": correct,
            "weight": weight,
        })

    score = (weighted_correct / total_weight * 10) if total_weight > 0 else 0

    return {
        "score": round(score, 2),
        "per_claim": per_claim,
        "weighted_correct": weighted_correct,
        "total_weight": total_weight,
    }


# --- Summary Scoring (LLM Judge) ---

def compute_summary_score_from_rubric(rubric: dict) -> float:
    """Compute summary score from judge rubric."""
    factual = rubric.get("factual_accuracy", 0)
    coverage = rubric.get("coverage", 0)
    no_inference = rubric.get("no_added_inference", 0)
    register = rubric.get("register_fluency", 0)
    verbatim = rubric.get("verbatim_penalty", 0)

    score = (
        factual / 3 * 3.5
        + coverage / 3 * 3.0
        + no_inference / 2 * 2.0
        + register / 2 * 1.5
        - verbatim * 1.0
    )
    return max(0, min(10, round(score, 2)))


# --- Coreference Scoring (Deterministic) ---

def compute_coref_score_from_rubric(rubric: dict) -> float:
    """Compute coreference score from judge rubric."""
    factual = rubric.get("factual_accuracy", 0)
    terminology = rubric.get("terminology_handling", 0)
    coverage = rubric.get("coverage", 0)
    no_inference = rubric.get("no_added_inference", 0)

    score = (
        factual / 3 * 4.0
        + terminology / 3 * 3.0
        + coverage / 2 * 2.0
        + no_inference / 2 * 1.0
    )
    return max(0, min(10, round(score, 2)))


def compute_coref_score(predicted: list[dict], reference: list[dict]) -> dict:
    """Compute coreference resolution score. Each item has span, referent, paragraph."""
    if not reference:
        return {"score": 0, "details": {"error": "No reference spans"}}

    matched = 0
    per_span = []

    for ref_item in reference:
        ref_span = normalize_arabic(ref_item.get("span", ""))
        ref_referent = ref_item.get("referent", "").lower().strip()

        best_match = False
        matched_pred = None
        for pred_item in predicted:
            pred_span = normalize_arabic(pred_item.get("span", ""))
            pred_referent = pred_item.get("referent", "").lower().strip()

            # Span match: exact or substring
            span_match = (pred_span == ref_span or
                         ref_span in pred_span or
                         pred_span in ref_span)
            # Referent match: check key terms (Omani/Yemeni side)
            referent_match = False
            for key in ["omani", "yemeni", "oman", "yemen"]:
                if key in ref_referent and key in pred_referent:
                    referent_match = True
                    break
            if not referent_match:
                referent_match = ref_referent == pred_referent

            if span_match and referent_match:
                best_match = True
                matched_pred = pred_item
                break

        if best_match:
            matched += 1

        per_span.append({
            "reference_span": ref_item.get("span", ""),
            "reference_referent": ref_item.get("referent", ""),
            "matched": best_match,
            "matched_prediction": matched_pred,
        })

    # Precision and recall
    precision = matched / len(predicted) if predicted else 1.0
    recall = matched / len(reference) if reference else 1.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    score = f1 * 10

    # Penalty for extra hallucinated spans
    extra = max(0, len(predicted) - len(reference))
    penalty = min(extra * 0.5, 2.0)
    score = max(0, score - penalty)

    return {
        "score": round(score, 2),
        "f1": round(f1, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "matched": matched,
        "total_reference": len(reference),
        "total_predicted": len(predicted),
        "penalty": penalty,
        "per_span": per_span,
    }


# --- Translation Scoring (LLM Judge) ---

def compute_translation_score_from_rubric(rubric: dict) -> float:
    """Compute translation score from judge rubric."""
    faithfulness = rubric.get("faithfulness", 0)
    fluency = rubric.get("fluency", 0)
    terminology = rubric.get("terminology", 0)
    register = rubric.get("register", 0)

    score = (
        faithfulness / 3 * 3.5
        + fluency / 3 * 3.0
        + terminology / 2 * 2.0
        + register / 2 * 1.5
    )
    return max(0, min(10, round(score, 2)))


# --- Overall Score ---

def compute_overall_score(ner: float, nli: float, summary: float, coref: float, translation: float = 0) -> float:
    return round(ner * 0.25 + nli * 0.20 + summary * 0.20 + coref * 0.15 + translation * 0.20, 2)


# --- High-level functions ---

def score_output(output: ModelOutput, db: Session) -> ScoreBreakdown:
    """Score all tasks for a single ModelOutput."""
    item = db.query(DatasetItem).filter(DatasetItem.id == output.dataset_item_id).first()
    article = db.query(Article).filter(Article.id == output.article_id).first()

    # NER
    ner_result = compute_ner_score(
        output.ner_output or {},
        item.ner_reference or {},
        article.body,
    )
    output.ner_score = ner_result["score"]

    # NLI
    nli_result = compute_nli_score(
        output.nli_output or [],
        item.nli_claims or [],
    )
    output.nli_score = nli_result["score"]

    # Coref (deterministic)
    coref_result = compute_coref_score(
        output.coref_output or [],
        item.coref_reference or [],
    )
    output.coref_score = coref_result["score"]

    # Summary score requires LLM judge - set to 0 if not judged yet
    if output.summary_score is None:
        output.summary_score = 0

    # Translation score requires LLM judge - set to 0 if not judged yet
    if output.translation_score is None:
        output.translation_score = 0

    output.overall_score = compute_overall_score(
        output.ner_score, output.nli_score, output.summary_score,
        output.coref_score, output.translation_score,
    )
    output.status = OutputStatus.SCORED
    db.commit()

    return ScoreBreakdown(
        task="all",
        score=output.overall_score,
        details={
            "ner": ner_result,
            "nli": nli_result,
            "coref": coref_result,
            "summary_score": output.summary_score,
        },
    )


def score_manual(item: DatasetItem, task: str, raw_output: str, db: Session) -> ScoreBreakdown:
    """Score a manually pasted output against a DatasetItem."""
    article = db.query(Article).filter(Article.id == item.article_id).first()

    if task == "ner":
        predicted = json.loads(raw_output) if isinstance(raw_output, str) else raw_output
        result = compute_ner_score(predicted, item.ner_reference or {}, article.body)
        return ScoreBreakdown(task="ner", score=result["score"], details=result)

    elif task == "nli":
        predicted = json.loads(raw_output) if isinstance(raw_output, str) else raw_output
        result = compute_nli_score(predicted, item.nli_claims or [])
        return ScoreBreakdown(task="nli", score=result["score"], details=result)

    elif task == "summary":
        return ScoreBreakdown(task="summary", score=0, details={"message": "Requires LLM judge"})

    elif task == "translation":
        return ScoreBreakdown(task="translation", score=0, details={"message": "Requires LLM judge"})

    elif task == "coref":
        predicted = json.loads(raw_output) if isinstance(raw_output, str) else raw_output
        result = compute_coref_score(predicted, item.coref_reference or [])
        return ScoreBreakdown(task="coref", score=result["score"], details=result)

    else:
        raise ValueError(f"Unknown task: {task}")


def score_run_task(run_id: str):
    """Score all outputs in a run (runs as background task)."""
    from database import SessionLocal
    db = SessionLocal()
    try:
        outputs = db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()
        for output in outputs:
            try:
                score_output(output, db)
            except Exception as e:
                output.status = OutputStatus.ERROR
                output.error_message = str(e)
                db.commit()
    finally:
        db.close()
