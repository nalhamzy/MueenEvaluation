# Human Evaluation — Process Guide

This folder contains everything needed to conduct a blinded human evaluation of the Arabic LLM benchmark, and everything produced when the evaluator returns the filled workbook.

---

## Files in this folder

| File | Purpose | Who sees it |
|------|---------|------------|
| `human_eval_workbook.xlsx` | The blinded scoring sheet for the evaluator | Evaluator + organizer |
| `human_eval_README.md` | This document (internal process guide) | Organizer only |
| `blinding_key.json` | Mapping of real model names → Model A/B/C/D | **Organizer only — keep private** |
| `sampled_articles.json` | The 30 article IDs used | Either |
| `evaluator_instructions.md` | Evaluator-facing instructions (safe to share) | Evaluator |

> **Important:** Do **not** send `blinding_key.json` to the evaluator. It reveals which anonymized column maps to which real model and would invalidate the whole exercise.

---

## Overview

**Goal.** Provide independent human judgment on the two LLM-judged tasks (Arabic Summary, English→Arabic Translation) to validate the automated GPT-5.2 judge used in the main benchmark.

**Sample.** 30 articles total, stratified as 6 per category (culture, finance, politics, sports, tech). All 4 models have complete outputs on all 30 articles.

**Tasks judged.**
- Summary (30 rows)
- Translation (30 rows)

**Total judgments produced.** 30 × 4 models × 2 tasks = **240 integer scores on a 1–5 scale**.

**Expected effort for the evaluator.** ~6 hours of focused work. Scoring is paced at ~90 seconds per model output.

**Not judged by human.** NER and NLI are scored deterministically against the reference (F1 with Arabic normalization, positional label accuracy). Human re-judgment adds no credibility there.

---

## End-to-end process

### Phase 1 — Prepare the package (organizer)

Regenerate the workbook from the database at any time:

```bash
py scripts/build_human_eval_package.py --seed 7 --per-category 6
```

Flags:
- `--seed N` — determines which articles are sampled and which letter each model gets. **Keep the seed constant** if you need to rerun.
- `--per-category N` — articles per category. Default 6 (= 30 total).
- `--out-dir DIR` — output folder, default `human_eval/`.

The builder only selects articles where all 4 models produced non-empty, scored Summary AND Translation outputs, so the evaluator never sees blank cells.

### Phase 2 — Hand off to evaluator (organizer)

Send the evaluator **only these two files**:

1. `human_eval_workbook.xlsx`
2. `evaluator_instructions.md`

Do not share `blinding_key.json`, `sampled_articles.json` (the category balance hints at nothing sensitive but is unnecessary), or any file in the project root that reveals model names alongside outputs (`mueen_results_full.json`, `comparison_data.csv`, `MUEEN_EVALUATION_REPORT_EN.md`, etc.).

Email / hand-off checklist:
- [ ] Attached `human_eval_workbook.xlsx`
- [ ] Attached `evaluator_instructions.md`
- [ ] Agreed deadline communicated
- [ ] Confirmed evaluator has Excel or compatible software
- [ ] Confirmed evaluator is a fluent/native Arabic reader
- [ ] Confirmed evaluator understands not to use any AI tool while scoring

### Phase 3 — Evaluator fills the workbook

The evaluator opens `human_eval_workbook.xlsx` and:
1. Reads the **Instructions** sheet.
2. Scores every row on the **Summary Task** sheet (30 rows × 4 scores each).
3. Scores every row on the **Translation Task** sheet (30 rows × 4 scores each).
4. Fills in the **Evaluator Info** sheet.
5. Saves and returns the file (same filename is fine).

The workbook enforces integer scores 1–5 via Excel data validation; invalid entries are rejected.

### Phase 4 — Ingest results (organizer)

Once the filled workbook comes back, place it at `human_eval/human_eval_workbook_filled.xlsx` (or any filename) and run:

```bash
py scripts/ingest_human_eval.py --filled human_eval/human_eval_workbook_filled.xlsx
```

This script (to be run **after** the workbook is returned) will:
1. Load the filled workbook and the private blinding key.
2. De-anonymize Model A/B/C/D → real model names.
3. Compute per-model mean + stdev on the 1–5 scale (Summary, Translation, and combined).
4. Rescale to 0–10 to compare directly with the GPT-5.2 judge scores from the main benchmark.
5. Compute **Spearman rank correlation** between human and GPT-5.2 ordering. This is the single most important credibility number.
6. Write `human_eval/human_eval_results.json` with all aggregates.
7. Emit a "Human Validation" Markdown block suitable for appending to `MUEEN_EVALUATION_REPORT_EN.md` and the Arabic letter.

### Phase 5 — Update report + letter

After ingestion:
1. Append the generated "Human Validation" section to `MUEEN_EVALUATION_REPORT_EN.md` under a new Section 4.5 or Section 8.
2. Add a new paragraph in `MUEEN_EVALUATION_LETTER_AR.md` (section رابعاً or a new خامساً) describing the human validation result in formal Arabic.
3. Bump `ATTACHMENTS_LIST.md` to include the human evaluation workbook + results as additional attachments.

Suggested wording for the updated letter (to adapt after results):
- If correlation is high (≥ 0.85): emphasize that human judgment confirms the ordering.
- If correlation is moderate (0.65–0.85): note that the human and automated judges broadly agree, with minor differences on specific tasks.
- If correlation is low (< 0.65): this is newsworthy — the report should highlight disagreement and recommend the human scores as the primary signal.

---

## Reproducibility

Anyone wanting to reproduce the evaluation needs:
- The SQLite DB with all scored runs (so the same 30 articles can be pulled)
- The seed (default `7`) to recreate identical article sampling and blinding

The seed is recorded in `blinding_key.json` and `sampled_articles.json`.

---

## Ethical / procedural notes

- The evaluator should be informed that their scores will be used as part of a formal evaluation report for the Mueen AI model.
- The evaluator should **not** be told which letter maps to which model, even informally, until after the workbook is returned and ingested.
- The evaluator's name and contact information (from the Evaluator Info sheet) should be quoted in the final report only with their permission.
- Single-evaluator design means we do NOT measure inter-rater reliability. If higher credibility is ever required, repeat the exercise with a second evaluator using a different seed (so articles overlap but not layouts) and compute Cohen's κ between the two sets of scores.
