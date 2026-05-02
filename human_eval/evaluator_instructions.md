# Instructions for the Evaluator

Thank you for agreeing to help with this evaluation. Please read this document in full **before** opening the workbook.

---

## What you are doing

You are evaluating the quality of Arabic language model outputs. You will score outputs from **four anonymous models** (labeled **Model A, Model B, Model C, Model D**) on two tasks:

1. **Arabic Summary** — given an Arabic news article, each model produced a short summary in formal Arabic (MSA / فصحى).
2. **English → Arabic Translation** — given a short English passage, each model translated it into Arabic.

Your judgment is being used to validate an automated benchmark. Please take it seriously.

---

## Very important — blinding

- You will **not** be told which letter maps to which real model. Please do not attempt to guess.
- If you happen to suspect a model based on style, **do not let that influence your score**. Score what is in front of you.
- The same letter refers to the same model throughout both task sheets — this is expected.
- Please do **not** discuss your scores with anyone else, search the internet for any output, or use any AI tool or translator to help you judge.

---

## How to score

Each cell gets an integer from **1 to 5**:

| Score | Meaning |
|:-----:|---------|
| **5** | **Excellent** — publication quality. Faithful to the source, fluent formal Arabic, no meaningful issues. |
| **4** | **Good** — Faithful and fluent. Minor issues only (small awkwardness, minor omission, small style issue). |
| **3** | **Acceptable** — Main content correct but clear issues (coverage gaps, some awkward phrasing, minor register slips). |
| **2** | **Poor** — Significant errors (notable factual issues, poor Arabic, missing key content). |
| **1** | **Unacceptable** — Factually wrong, unreadable, or unusable as Arabic output. Also use 1 for empty or cut-off outputs. |

**The workbook enforces integers 1–5.** Decimals and blanks are rejected.

### Score Summary outputs on:
- **Factual accuracy** — does the summary state only things actually in the article?
- **Coverage** — does it capture the main events/points?
- **Conciseness & register** — is it formal MSA and appropriately short?
- **Invention penalty** — added details not in the article = factual error.

### Score Translation outputs on:
- **Faithfulness** — does the Arabic say exactly what the English says, nothing more, nothing less?
- **Fluency** — does it read as natural, formal Arabic?
- **Terminology** — are proper nouns, technical terms, numbers handled correctly?
- **Register** — formal MSA. Noticeable dialect = register issue.

---

## Process

1. **Open the file.** It has four sheets: `Instructions`, `Summary Task`, `Translation Task`, `Evaluator Info`.
2. **Read the `Instructions` sheet first** — it is a shorter version of this document inside the workbook.
3. **Complete the `Summary Task` sheet.** For each of the 30 rows:
   - Read the Arabic **Article** (column D).
   - Read the **Reference Arabic** summary (column E) — this is what a strong teacher model produced. Use it only as one reference point; don't treat it as the gold standard that Model X must match. Score each model on its own merits against the article.
   - Read each of the 4 model outputs in columns F–I.
   - Enter 4 integer scores in columns J–M (yellow cells).
   - Optionally add a note in column N (e.g., "B invented a date", "A cut off mid-sentence").
4. **Complete the `Translation Task` sheet** the same way. Here column D is the English source, column E is the reference Arabic translation, and columns F–I are the four model translations.
5. **Fill in the `Evaluator Info` sheet** — your name, dates, total hours, Arabic proficiency, your own confidence in your scoring (1–5), and any general feedback.
6. **Save** the file (.xlsx) and return it to the person who sent it to you.

---

## Do ✅

- Score each row **independently**. Do not let earlier rows anchor your judgment.
- **Take breaks.** This is ~6 hours of focused work. Splitting over 2–3 sessions is recommended.
- **Score all 4 columns on every row**, even when outputs look similar. Differences are often subtle.
- When an output is **empty or cut off mid-sentence**, give it a score of **1** and note it.
- Use the **Notes** column freely — your observations help us interpret the numbers.
- If you think the article itself is problematic (corrupted, unreadable Arabic source), score a 1 across that row and note it — this happens rarely.

## Do NOT ❌

- Do not try to guess which letter is which model.
- Do not discuss scores with anyone while you are working.
- Do not use ChatGPT, Claude, Google Translate, or any AI tool to help you judge.
- Do not leave score cells blank.
- Do not modify column positions, insert/delete rows, or add new sheets.

---

## Time estimate

| Sheet | Rows | ~Time per row | Total |
|-------|:----:|:-------------:|:-----:|
| Summary Task | 30 | ~5 min | ~2.5 hr |
| Translation Task | 30 | ~5 min | ~2.5 hr |
| Evaluator Info + review | — | — | ~0.5 hr |
| **Total** | | | **~5.5–6 hours** |

---

## Questions

If something about a specific row is truly ambiguous, score it on your best judgment and note the ambiguity in the Notes column. For **process** questions (file won't open, scores not saving, etc.), contact the person who sent you the workbook — **do not** ask about the meaning of scores, models, or outputs.

Thank you.
