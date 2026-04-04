# Scoring Service

## Overview

The scoring service evaluates LLM outputs against reference data using two methods:
- **Deterministic scoring** for NER, NLI, and Coreference (exact computation, no LLM needed)
- **LLM-as-Judge** for Summary (requires judge model call)

## Score Weights

```
Overall = NER × 0.30 + NLI × 0.25 + Summary × 0.25 + Coref × 0.20
```

All individual scores are on a 0–10 scale.

## NER Scoring (Deterministic)

### Algorithm

1. **Normalize** all entity strings (both predicted and reference):
   - Remove Arabic diacritics (tashkeel: `\u064B-\u065F`, `\u0670`)
   - Normalize alef variants (`إأآا` → `ا`)
   - Remove definite article (`ال`) prefix
   - Strip punctuation, collapse whitespace, lowercase

2. **Per-category F1** for PERSON, LOCATION, ORGANIZATION, MISC:
   ```
   TP = |predicted ∩ reference|
   FP = |predicted| - TP
   FN = |reference| - TP
   F1 = 2 × precision × recall / (precision + recall)
   ```
   Edge case: if both sets empty → F1 = 1.0 (nothing to predict, nothing missed)

3. **Weighted average**:
   ```
   PERSON:       0.35  (hardest, most discriminating)
   LOCATION:     0.25
   ORGANIZATION: 0.25
   MISC:         0.15
   ```

4. **Hallucination penalty**: For each predicted entity not found in the article body text → -1.5 points (capped at -3.0 total)

5. **Final**: `score = max(0, weighted_f1 × 10 - penalty)`

### Why These Weights?

Person names in Arabic are the hardest to extract correctly due to morphological variation, so they get the highest weight. MISC entities (weapons, quantities) are more formulaic, hence lowest weight.

## NLI Scoring (Deterministic)

### Algorithm

1. **Match by position**: Reference claim `i` is compared to predicted claim `i`
2. **Weighted exact match**:
   ```
   NOT_ENOUGH_INFO: weight = 1.5  (hardest to get right)
   REFUTED:         weight = 1.2
   SUPPORTED:       weight = 1.0
   ```
3. **Score**: `sum(correct × weight) / sum(all weights) × 10`

### Why Positional Matching?

Claims are generated in a fixed order by the teacher LLM. The student receives the same claims and must label each one, so positional alignment is guaranteed.

## Summary Scoring (LLM Judge)

### Rubric

| Criterion | Range | Weight | Description |
|-----------|-------|--------|-------------|
| `factual_accuracy` | 0–3 | 3.5 | Hallucination check against source |
| `coverage` | 0–3 | 3.0 | Key events covered |
| `no_added_inference` | 0–2 | 2.0 | No unsourced conclusions |
| `register_fluency` | 0–2 | 1.5 | Formal MSA throughout |
| `verbatim_penalty` | 0–1 | -1.0 | Penalty for copied sentences |

### Formula

```python
score = (factual/3 × 3.5 + coverage/3 × 3.0 + inference/2 × 2.0 + register/2 × 1.5 - verbatim × 1.0)
# Clamped to [0, 10]
```

Maximum possible: 3.5 + 3.0 + 2.0 + 1.5 = **10.0**

## Entity Coreference Resolution Scoring (Deterministic)

### Algorithm

1. **Parse** both predicted and reference JSON arrays of `{span, referent, paragraph}` objects.

2. **Match** predicted mentions to reference mentions by exact `(span, referent)` tuple equality (after Arabic normalization on `span`).

3. **Compute F1** over matched mention tuples:
   ```
   TP = |predicted ∩ reference|   (by span+referent)
   FP = |predicted| - TP
   FN = |reference| - TP
   F1 = 2 × precision × recall / (precision + recall)
   ```
   Edge case: if both sets empty → F1 = 1.0

4. **Hallucination penalty**: For each predicted span not found anywhere in the article body text → -1.0 point (capped at -3.0 total).

5. **Final**: `score = max(0, F1 × 10 - penalty)`

## Manual Scoring

The `POST /api/scoring/score-manual` endpoint allows pasting raw LLM output and scoring it against any article's DatasetItem without running a full evaluation.

**Request**:
```json
{
  "article_id": "ART_001",
  "task": "ner",
  "model_output": "{\"PERSON\": [\"محمد\"], \"LOCATION\": [], \"ORGANIZATION\": [], \"MISC\": []}"
}
```

**Response**: Full score breakdown with per-category metrics.

## Implementation

**File**: `backend/services/scoring_service.py`

Key functions:
- `normalize_arabic(text)` — Arabic text normalization for comparison
- `compute_ner_score(predicted, reference, article_body)` — Full NER F1 with penalty
- `compute_nli_score(predicted, reference)` — Weighted NLI accuracy
- `compute_summary_score_from_rubric(rubric)` — Score from judge rubric
- `compute_coref_score(predicted, reference, article_body)` — Deterministic F1 with hallucination penalty
- `compute_overall_score(ner, nli, summary, coref)` — Weighted average

## Testing

```bash
py -m pytest backend/tests/test_scoring.py -v
```

16 tests covering:
- Arabic normalization (diacritics, alef, definite article, punctuation)
- NER scoring (perfect, zero, partial, hallucination penalty)
- NLI scoring (perfect, zero, partial, weighted label importance)
- Rubric computation (summary)
- Coref scoring (perfect, zero, partial, hallucination penalty)
- Overall score weights
