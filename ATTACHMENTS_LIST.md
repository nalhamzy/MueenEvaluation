# Attachments — Mueen AI Evaluation Delivery Package

**Prepared:** 2026-04-16
**Updated:** 2026-05-02 (added human validation, bootstrap CIs, limitations, methodology, executive brief)
**Cover letter:** `MUEEN_EVALUATION_LETTER_AR.md` (Arabic)
**Purpose:** Formal evaluation results of Mueen AI delivered to the requesting authority.

---

## Quick reference — what to read in what order

| Audience | Read first | Read next |
|----------|------------|-----------|
| Senior executive (Arabic) | `EXECUTIVE_BRIEF_AR.md` (1 page) | `MUEEN_EVALUATION_LETTER_AR.md` |
| Decision-maker reviewing the cover letter | `MUEEN_EVALUATION_LETTER_AR.md` | `LIMITATIONS.md` |
| Technical reviewer | `MUEEN_EVALUATION_REPORT_EN.md` | `METHODOLOGY.md` + `LIMITATIONS.md` |
| Mueen engineering team | Section 7 of report (Recommendations) | `mueen_evaluation_samples.md` |
| Auditor / reproducibility check | `METHODOLOGY.md` | `bootstrap_ci.json` + `human_eval/` |

---

## Attachment 1 — Arabic Executive Brief (1 page)

**File:** `EXECUTIVE_BRIEF_AR.md`

A single-page Arabic summary suitable for senior decision-makers. Contains the headline result, the human validation summary, top 3 weaknesses, and prioritized recommendations.

**Audience:** Executive stakeholders. **Time to read:** 2 minutes.

---

## Attachment 2 — Arabic Cover Letter (Official)

**File:** `MUEEN_EVALUATION_LETTER_AR.md`

The formal Arabic letter (governmental register) presenting the full evaluation results, including:
- Results with 95% confidence intervals
- Independent human validation findings
- Limitations and caveats
- Prioritized recommendations
- Conclusion

**Audience:** Requesting authority. **Time to read:** 15 minutes.

---

## Attachment 3 — Full Technical Report (English)

**File:** `MUEEN_EVALUATION_REPORT_EN.md`

Comprehensive English technical report covering:
- Executive summary with statistically-validated leaderboard
- Description of all four models (including known/unknown attributes)
- Full methodology (architecture, 4 tasks, scoring formulas, statistical methodology)
- Detailed results with 95% bootstrap CIs and pairwise significance
- Mueen AI deep-dive (strengths, weaknesses, failure patterns)
- Prioritized recommendations
- Section 8 — Independent Human Validation (240 judgments)
- Section 9 — Limitations and threats to validity (9 enumerated)
- Reproducibility section

**Audience:** Technical reviewers. **Time to read:** 45 minutes.

---

## Attachment 4 — Cross-Model Comparison Report

**File:** `200-ARTICLE-EVALUATION.md`

Stand-alone document comparing all four evaluated models on the 200-article set. Includes per-task breakdowns, per-category breakdowns, and a stability analysis comparing 100 vs. 200 article evaluation rounds (the within-study reliability check).

---

## Attachment 5 — Methodology Document

**File:** `METHODOLOGY.md`

Standalone description of the benchmark architecture, dataset, four tasks, scoring formulas, statistical methodology (bootstrap, Spearman), infrastructure, and reproduction recipe. Suitable for academic or technical-audit review.

---

## Attachment 6 — Limitations Document

**File:** `LIMITATIONS.md`

Standalone enumeration of every methodological limitation an independent reviewer could reasonably raise about this evaluation, with severity, impact, and recommended mitigation for each. Provided as a separate file so that any reviewer has a single authoritative reference for known weaknesses.

**The 9 documented limitations:**
1. Single human evaluator (no inter-rater reliability)
2. Browser-based vs. API-based evaluation asymmetry for Mueen
3. Reference data from a single LLM (Claude Opus 4.6)
4. LLM judge absolute calibration gap
5. Score weights not formally optimized
6. Small per-category sample sizes
7. Translation direction unidirectional
8. Evaluator domain expertise undocumented
9. Benchmarks ≠ comprehensive evaluations

---

## Attachment 7 — Worked Side-by-Side Examples

**File:** `mueen_evaluation_samples.md`

Five real evaluation examples (one per category, picked at the per-category median Mueen score). Each example shows:
- Article excerpt in Arabic
- Mueen's NER output vs. Claude Opus reference
- Mueen's summary vs. reference (with judge rubric)
- Mueen's NLI labels vs. ground truth (per claim)
- Mueen's translation vs. reference (with judge rubric)

---

## Attachment 8 — Mueen Full Results (raw data)

**File:** `mueen_results_full.json`

JSON with one record per evaluated article, containing: article ID, category, title, all four task scores, all four Mueen outputs, all four reference outputs (from Claude Opus), and the GPT-5.2 judge rubrics for summary and translation. Suitable for re-analysis or external auditing.

---

## Attachment 9 — Machine-Readable Comparison Data

**File:** `comparison_data.csv`

CSV (UTF-8 BOM, Excel-compatible) with one row per (model, article) combination across all 4 models and 200 articles. Columns: model_name, article_id, category, ner_score, nli_score, summary_score, translation_score, overall_score. ~800 rows.

---

## Attachment 10 — Bootstrap Confidence Intervals (raw data)

**File:** `bootstrap_ci.json`

Machine-readable file with the full bootstrap CI computation: per model × per task, n articles, point estimate (mean), 2.5th and 97.5th percentile bounds, and CI half-width. 1000 iterations, seed=11.

---

## Attachment 11 — Filled Human Evaluation Workbook

**File:** `human_eval/human_eval_workbook_Ahmed.xlsx`

The blinded scoring workbook completed by an independent human evaluator (Ahmed Al Saidi, native Arabic speaker) over the period 2026-04-28 → 2026-05-02. Contains:
- 30 articles × 4 anonymized models × 2 tasks (Summary, Translation) = 240 integer scores on a 1–5 scale
- Per-row qualitative notes by the evaluator
- Evaluator's general observations

The blinding key (`human_eval/blinding_key.json`) is available on request but was withheld from the evaluator until scoring was complete. Mapping: A = Qwen 3.5, B = Mueen AI, C = DeepSeek Chat, D = Mistral Large.

---

## Attachment 12 — Human Evaluation Aggregated Results

**File:** `human_eval/human_eval_results.json`

JSON with the post-ingestion aggregates:
- Per-model means (Summary, Translation, Combined) on both 1–5 and 0–10 scales
- Per-category breakdowns
- Spearman and Pearson correlations between human and GPT-5.2 LLM judge per task and combined
- Model-level rank comparison (4-point Spearman)
- Evaluator metadata

---

## Attachment 13 — Human Evaluation Long-Form Scores

**File:** `human_eval/human_eval_results.csv`

CSV (UTF-8 BOM, Excel-compatible) with one row per (article, model, task) — 240 rows. Columns: article_id, category, task, model, model_display, human_1_5, human_0_10, llm_judge_0_10. Enables direct re-analysis of the human evaluation against the LLM judge scores.

---

## Attachment 14 — This Attachments List

**File:** `ATTACHMENTS_LIST.md`

The current document — formal index of all attachments in this delivery package.

---

## Document version history

| Version | Date | Changes |
|---------|------|---------|
| v1 | 2026-04-16 | Initial release. 6 attachments: report (EN), letter (AR), 200-article comparison, samples, raw Mueen results, CSV, list |
| **v2** | **2026-05-02** | **Added human validation (Section 8 + 3 attachments). Added bootstrap CIs to all tables. Created standalone LIMITATIONS.md and METHODOLOGY.md. Added Arabic executive brief. Updated cover letter to reflect full updates. Total attachments: 14.** |

---

## File integrity (optional)

Recipients may verify file integrity by computing SHA-256 of each attachment:

```bash
sha256sum EXECUTIVE_BRIEF_AR.md \
          MUEEN_EVALUATION_LETTER_AR.md \
          MUEEN_EVALUATION_REPORT_EN.md \
          200-ARTICLE-EVALUATION.md \
          METHODOLOGY.md \
          LIMITATIONS.md \
          mueen_evaluation_samples.md \
          mueen_results_full.json \
          comparison_data.csv \
          bootstrap_ci.json \
          human_eval/human_eval_workbook_Ahmed.xlsx \
          human_eval/human_eval_results.json \
          human_eval/human_eval_results.csv \
          ATTACHMENTS_LIST.md
```
