# Attachments — Mueen AI Evaluation Delivery Package

**Prepared:** 2026-04-16  
**Cover letter:** `MUEEN_EVALUATION_LETTER_AR.md` (Arabic)  
**Purpose:** Formal evaluation results of Mueen AI delivered to the requesting authority.

---

## Attachment 1 — Full Technical Report (English)

**File:** `MUEEN_EVALUATION_REPORT_EN.md`

Comprehensive technical report covering:
- Executive summary with leaderboard
- Evaluation methodology (architecture, 4 tasks, scoring formulas)
- Full per-task and per-category results for all 4 models
- Mueen AI deep-dive (strengths, weaknesses, failure patterns)
- Prioritized recommendations for the Mueen team

---

## Attachment 2 — Cross-Model Comparison Report

**File:** `200-ARTICLE-EVALUATION.md`

Stand-alone document comparing all four evaluated models on the 200-article set: Qwen 3.5 397B, DeepSeek Chat (V3), Mistral Large, Mueen AI. Includes per-task breakdowns, per-category breakdowns, and a stability analysis comparing 100 vs 200 article evaluation rounds.

---

## Attachment 3 — Worked Side-by-Side Examples

**File:** `mueen_evaluation_samples.md`

Five real evaluation examples (one per category, picked at the per-category median Mueen score). Each example shows:
- Article excerpt in Arabic
- Mueen's NER output vs Claude Opus reference
- Mueen's summary vs reference (with judge rubric)
- Mueen's NLI labels vs ground truth (per claim)
- Mueen's translation vs reference (with judge rubric)

---

## Attachment 4 — Mueen Full Results (raw data)

**File:** `mueen_results_full.json`

JSON file containing one record per evaluated article with: article ID, category, title, all four task scores, all four Mueen outputs, all four reference outputs (from Claude Opus), and the GPT-5.2 judge rubrics for summary and translation. Suitable for re-analysis or external auditing.

---

## Attachment 5 — Machine-Readable Comparison Data

**File:** `comparison_data.csv`

CSV file with one row per (model, article) combination across all 4 models and 200 articles. Columns: model_name, article_id, category, ner_score, nli_score, summary_score, translation_score, overall_score. Total ~800 rows. Encoded as UTF-8 with BOM for Excel compatibility.

---

## Attachment 6 — This Attachments List

**File:** `ATTACHMENTS_LIST.md`

The current document — a formal index of all attachments in this delivery package.

---

## File integrity checksum (optional)

Recipients may verify file integrity by computing SHA-256 of each file:

```bash
sha256sum MUEEN_EVALUATION_REPORT_EN.md \
          200-ARTICLE-EVALUATION.md \
          mueen_evaluation_samples.md \
          mueen_results_full.json \
          comparison_data.csv \
          ATTACHMENTS_LIST.md
```