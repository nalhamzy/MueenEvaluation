# Arabic LLM Benchmark Platform — Full Build Instructions

> Hand this document to an AI coding assistant (Cursor, Copilot, Claude Code, etc.) as the
> complete specification. Every section is intentional — do not skip or summarise any part.

---
REQUIRED : 
* EACH FEATURE MUST BE TESTED , DOCUMENTED RESULT . EX LOAD CSV , PREPROCESSING ETC 
## 1. Project Overview

Build a full-stack platform that:
1. Ingests a CSV of 100 Arabic news articles
2. Generates a structured evaluation dataset from those articles using a Teacher LLM
3. Runs the dataset against one or more Student LLMs via OpenAI-compatible APIs
4. Scores each model output using deterministic metrics AND an LLM-as-Judge
5. Displays all results in a real-time Angular dashboard with charts, per-article drill-down,
   and an AI-generated executive summary report

**Stack:**
- Backend: Python 3.11+ (FastAPI)
- Frontend: Angular 17+ (standalone components, Angular Material)
- Database: SQLite (via SQLAlchemy, upgradeable to PostgreSQL)
- Task queue: Celery + Redis (for async LLM jobs)
- LLM calls: OpenAI Python SDK (compatible with any OpenAI-API-format endpoint)

---

## 2. Input Format

### 2.1 CSV Schema
The input CSV file has the following columns. All text fields are UTF-8 Arabic.

```
article_id   : string  — unique identifier (e.g. "ART_001")
title        : string  — article headline in Arabic
body         : string  — full article text in Arabic
source       : string  — publication name
date         : string  — ISO 8601 date (YYYY-MM-DD)
```

### 2.2 LLM Configuration (provided at runtime via UI or .env)
```
TEACHER_MODEL       : model string for dataset generation (e.g. "gpt-4o")
TEACHER_API_KEY     : OpenAI API key for teacher
STUDENT_MODELS      : comma-separated list (e.g. "gpt-4o-mini,gpt-3.5-turbo,mistral-large")
STUDENT_API_KEY     : API key(s) — either one shared key or per-model in a JSON map
JUDGE_MODEL         : model used as LLM-as-Judge (e.g. "gpt-4o")
JUDGE_API_KEY       : API key for judge (can be same as teacher)
OPENAI_BASE_URL     : optional — override for non-OpenAI endpoints
```

---

## 3. Data Models (SQLAlchemy)

Create the following tables. Use Alembic for migrations.

### Article
```
id              : String PK
title           : Text
body            : Text
source          : String
date            : Date
status          : Enum(PENDING, GENERATING, READY, ERROR)
created_at      : DateTime
```

### DatasetItem
One article produces exactly one DatasetItem containing all four tasks.
```
id              : UUID PK
article_id      : FK -> Article
ner_input       : Text  (the article excerpt used as NER input)
ner_reference   : JSON  ({"PERSON":[], "LOCATION":[], "ORGANIZATION":[], "MISC":[]})
summary_input   : Text  (full article body)
summary_reference : Text (2-sentence فصحى reference summary)
nli_input       : Text  (article body)
nli_claims      : JSON  (list of {"claim": str, "label": "SUPPORTED"|"REFUTED"|"NOT_ENOUGH_INFO"})
                         — minimum 3 claims per article, at least 1 of each label
xling_input     : Text  (article body)
xling_reference : Text  (3-bullet English intelligence brief)
generated_at    : DateTime
teacher_model   : String
```

### EvaluationRun
One run = one model evaluated against the full dataset.
```
id              : UUID PK
model_name      : String
api_base_url    : String (nullable)
status          : Enum(QUEUED, RUNNING, COMPLETED, FAILED)
started_at      : DateTime
completed_at    : DateTime (nullable)
total_articles  : Integer
processed_count : Integer
error_message   : Text (nullable)
```

### ModelOutput
One row per (DatasetItem × EvaluationRun).
```
id              : UUID PK
run_id          : FK -> EvaluationRun
dataset_item_id : FK -> DatasetItem
article_id      : FK -> Article

ner_output      : JSON  (same schema as ner_reference)
summary_output  : Text
nli_output      : JSON  (list of {"claim": str, "label": str})
xling_output    : Text

ner_score       : Float  (0–10, computed deterministically)
summary_score   : Float  (0–10, from LLM judge)
nli_score       : Float  (0–10, computed deterministically)
xling_score     : Float  (0–10, from LLM judge)
overall_score   : Float  (weighted average)

judge_summary_rubric    : JSON  (raw judge rubric breakdown)
judge_xling_rubric      : JSON  (raw judge rubric breakdown)

status          : Enum(PENDING, RUNNING, SCORED, ERROR)
error_message   : Text (nullable)
processed_at    : DateTime (nullable)
```

### ExecutiveSummary
```
id              : UUID PK
run_id          : FK -> EvaluationRun (nullable — null = cross-model comparison)
content         : Text  (markdown)
generated_at    : DateTime
```

---

## 4. Backend — FastAPI Application Structure

```
backend/
├── main.py
├── config.py           (pydantic BaseSettings, reads .env)
├── database.py         (SQLAlchemy engine + session)
├── models.py           (all SQLAlchemy models)
├── schemas.py          (all Pydantic request/response schemas)
├── celery_app.py       (Celery + Redis config)
├── routers/
│   ├── articles.py
│   ├── dataset.py
│   ├── runs.py
│   ├── outputs.py
│   ├── scoring.py
│   └── reports.py
├── services/
│   ├── teacher_service.py    (dataset generation prompts + calls)
│   ├── student_service.py    (model evaluation calls)
│   ├── scoring_service.py    (deterministic + judge scoring)
│   ├── report_service.py     (executive summary generation)
│   └── csv_service.py        (CSV ingest + validation)
└── tasks/
    ├── generate_dataset.py   (Celery tasks)
    ├── run_evaluation.py
    └── score_outputs.py
```

### 4.1 API Endpoints

**Articles**
```
POST   /api/articles/upload          — upload CSV, parse, insert articles
GET    /api/articles                 — list all articles with status
GET    /api/articles/{id}            — single article detail
```

**Dataset**
```
POST   /api/dataset/generate         — trigger Teacher LLM generation for all PENDING articles
GET    /api/dataset                  — list all DatasetItems
GET    /api/dataset/{article_id}     — DatasetItem for a specific article
GET    /api/dataset/stats            — counts by task type, completion rate
```

**Evaluation Runs**
```
POST   /api/runs                     — create new run (body: {model_name, api_key, base_url})
GET    /api/runs                     — list all runs with status + progress
GET    /api/runs/{id}                — single run detail + per-article breakdown
DELETE /api/runs/{id}                — cancel a queued/running run
```

**Outputs & Scoring**
```
GET    /api/outputs/{run_id}                     — all outputs for a run
GET    /api/outputs/{run_id}/{article_id}        — single output detail with scores
POST   /api/scoring/score-output                 — manually trigger scoring for one ModelOutput
POST   /api/scoring/score-run/{run_id}           — trigger scoring for entire run
POST   /api/scoring/judge/{output_id}            — re-run LLM judge on one output
```

**Reports**
```
GET    /api/reports/summary/{run_id}             — executive summary for one run
POST   /api/reports/generate/{run_id}            — generate/regenerate executive summary
GET    /api/reports/comparison                   — cross-model comparison stats
GET    /api/reports/export/{run_id}              — download JSON report
```

**Config**
```
GET    /api/config                   — current LLM config (keys masked)
PUT    /api/config                   — update LLM config
```

---

## 5. Teacher LLM — Dataset Generation

### 5.1 NER Generation Prompt
```
SYSTEM:
You are an expert Arabic NLP annotator. Your output must be valid JSON only.
No preamble. No markdown fences. No explanation.

USER:
Given the following Arabic news article, extract all named entities and return
a JSON object with exactly these four keys:
  "PERSON"       — named individuals only (not titles like وزير or رئيس alone)
  "LOCATION"     — geographic places, border crossings, regions, bodies of water
  "ORGANIZATION" — government bodies, militias, companies, agencies
  "MISC"         — weapons, equipment, vehicles, numbered quantities of physical items

Rules:
1. Extract only entities that appear in the text. Do not infer or add entities not present.
2. For PERSON: include full name as it appears. Do not extract generic titles without a name.
3. For ORGANIZATION: if an organization has both an Arabic name and an acronym in the text,
   list the full name only. Do not duplicate as two entries.
4. For LOCATION: if the same place is described with varying specificity
   (e.g. "منفذ صرفيت" and "منفذ صرفيت بمحافظة المهرة"), list the most specific form.
5. Deduplicate: do not list morphological variants (definite/indefinite) as separate entities.
6. Return JSON only. No other text.

Article:
{article_body}
```

### 5.2 Abstractive Summary Generation Prompt
```
SYSTEM:
You are an expert Arabic news analyst. Write only in formal Modern Standard Arabic (فصحى).
No dialect. No code-switching. No English words. Output the summary only — no labels,
no preamble.

USER:
Summarize the following Arabic news article in exactly 2 sentences in formal Arabic (فصحى).

Rules:
1. Do not copy any sentence verbatim from the source. Rephrase all content.
2. Cover the most important events. Prioritize named actors, locations, and actions.
3. Do not add analysis, conclusions, or opinions not explicitly stated in the article.
   (Do not write phrases like "مما يعكس..." or "وهو ما يدل على..." unless sourced.)
4. Maintain formal register throughout. No colloquial expressions.
5. Do not mention the word "المقال" or "التقرير" — write as if briefing a colleague directly.

Article:
{article_body}
```

### 5.3 NLI Claims Generation Prompt
```
SYSTEM:
You are an expert fact-checking annotator for Arabic news. Output valid JSON only.
No markdown. No preamble.

USER:
Given the following Arabic news article, generate exactly 4 claim-label pairs for
a Natural Language Inference (NLI) fact-verification benchmark.

Requirements:
- Exactly 2 claims labelled "SUPPORTED" (clearly supported by the text)
- Exactly 1 claim labelled "REFUTED" (directly contradicted by the text)
- Exactly 1 claim labelled "NOT_ENOUGH_INFO" (plausible but not confirmed by the text)

Hard rules:
1. All claims must be written in Arabic.
2. The REFUTED claim must be a subtle distortion of a fact in the text
   (e.g. wrong number, wrong location, wrong actor) — not an obvious fabrication.
3. The NOT_ENOUGH_INFO claim must be plausible and related to the article's topic
   but genuinely absent from the text.
4. Do not use phrases from the article verbatim in the claims — paraphrase.
5. Return JSON array: [{"claim": "...", "label": "SUPPORTED|REFUTED|NOT_ENOUGH_INFO"}, ...]

Article:
{article_body}
```

### 5.4 Cross-Lingual Mapping Generation Prompt
```
SYSTEM:
You are a senior intelligence analyst fluent in Arabic and English.
Write only English. Output the brief only — no labels, no preamble.

USER:
Write a 3-bullet English intelligence brief based on the following Arabic news article.

Rules:
1. Each bullet must cover a distinct event or development from the article.
2. For any GCC-specific term, Arabic proper noun, or concept with no direct English
   equivalent, provide the Arabic original in square brackets immediately after the
   English rendering. Example: Sarfait Crossing [منفذ صرفيت].
3. Do not add analysis or inference beyond what the article explicitly states.
4. Do not omit named actors, specific locations, quantities, or weapon types
   that appear in the article.
5. Write each bullet as a single complete sentence. No sub-bullets.
6. Target audience: a non-Arabic-speaking senior analyst with no regional background.

Article:
{article_body}
```

---

## 6. Student LLM — Evaluation Prompts

When running a student model, send each task with the same prompts as Section 5
but **replace the reference article with the DatasetItem's stored input field**
(not the full article — use exactly what was used to generate the reference).

For NER and NLI tasks, set `response_format={"type": "json_object"}` if the model
supports it. Otherwise, strip markdown fences before parsing.

---

## 7. Scoring Service

### 7.1 NER Scoring (Deterministic, 0–10)

Compute per-category F1 using token-level exact match after normalization.

**Normalization function** (apply to all entity strings before comparison):
```python
import re, unicodedata

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
```

**Per-category scoring:**
```
For each category in [PERSON, LOCATION, ORGANIZATION, MISC]:
  normalize all reference entities
  normalize all predicted entities
  TP = |predicted ∩ reference|
  FP = |predicted| - TP
  FN = |reference| - TP
  precision = TP / (TP + FP) if (TP + FP) > 0 else 1.0
  recall    = TP / (TP + FN) if (TP + FN) > 0 else 1.0
  f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
```

**Overall NER score:**
```
Weighted F1:
  PERSON       weight = 0.35  (hardest, most discriminating)
  LOCATION     weight = 0.25
  ORGANIZATION weight = 0.25
  MISC         weight = 0.15

ner_score = sum(category_f1 * weight) * 10   (scale to 0–10)

Penalty: if any hallucinated entity exists (entity in predicted but NOT in article body
after search), subtract 1.5 points per hallucination, capped at -3.0 total.
```

### 7.2 NLI Scoring (Deterministic, 0–10)
```
For each claim in the dataset:
  predicted_label = model output label for that claim
  reference_label = stored label in DatasetItem

  exact_match = 1 if predicted_label == reference_label else 0

  Per-label weights:
    NOT_ENOUGH_INFO matches: weight = 1.5  (hardest to get right)
    REFUTED matches:         weight = 1.2
    SUPPORTED matches:       weight = 1.0

weighted_score = sum(exact_match * weight) / sum(all weights)
nli_score = weighted_score * 10
```

### 7.3 Summary Scoring — LLM as Judge (0–10)

Send the following to the JUDGE_MODEL:
```
SYSTEM:
You are an expert evaluator of Arabic text summarization. Return valid JSON only.
No preamble. No markdown.

USER:
Score the following Arabic summary against the reference and source article.

SOURCE ARTICLE:
{article_body}

REFERENCE SUMMARY (gold standard):
{summary_reference}

MODEL SUMMARY (to evaluate):
{summary_output}

Return a JSON object with these exact keys:
{
  "factual_accuracy":   integer 0–3,  // 0=hallucination, 1=partially correct, 2=mostly correct, 3=fully grounded
  "coverage":           integer 0–3,  // 0=misses key events, 1=partial, 2=good, 3=all key events covered
  "no_added_inference": integer 0–2,  // 0=adds unsourced conclusions, 1=minor, 2=fully grounded
  "register_fluency":   integer 0–2,  // 0=dialect/code-switch/errors, 1=acceptable, 2=formal فصحى throughout
  "verbatim_penalty":   integer 0–1,  // 1 if more than 2 consecutive sentences copied from source, else 0
  "reasoning":          string        // one sentence explaining the score
}
```

Compute: `summary_score = (factual_accuracy/3 * 3.5 + coverage/3 * 3.0 + no_added_inference/2 * 2.0 + register_fluency/2 * 1.5 - verbatim_penalty * 1.0)`

Scale to 0–10. Clamp to [0, 10].

### 7.4 Cross-Lingual Scoring — LLM as Judge (0–10)

```
SYSTEM:
You are an expert bilingual Arabic-English intelligence analyst and evaluator.
Return valid JSON only. No preamble. No markdown.

USER:
Score the following English intelligence brief against the reference and Arabic source.

ARABIC SOURCE ARTICLE:
{article_body}

REFERENCE BRIEF (gold standard):
{xling_reference}

MODEL BRIEF (to evaluate):
{xling_output}

Return JSON:
{
  "factual_accuracy":        integer 0–3,  // facts match Arabic source
  "terminology_handling":    integer 0–3,  // GCC/Arabic terms correctly rendered + bracketed
  "coverage":                integer 0–2,  // all key events represented
  "no_added_inference":      integer 0–2,  // no unsourced analysis added
  "reasoning":               string
}
```

Compute: `xling_score = (factual_accuracy/3 * 4.0 + terminology_handling/3 * 3.0 + coverage/2 * 2.0 + no_added_inference/2 * 1.0)`

Scale to 0–10. Clamp to [0, 10].

### 7.5 Overall Score
```
overall_score = (
  ner_score   * 0.30 +
  nli_score   * 0.25 +
  summary_score * 0.25 +
  xling_score * 0.20
)
```

---

## 8. Manual Scoring Feature

The system must support pasting an LLM output directly into the UI and running
the scorer against a specific article's DatasetItem without running a full evaluation.

**Endpoint:** `POST /api/scoring/score-manual`

Request body:
```json
{
  "article_id":      "ART_001",
  "task":            "ner | summary | nli | xling",
  "model_output":    "raw string or JSON string from the LLM"
}
```

Response: full score breakdown including per-category metrics and judge rubric
(for summary/xling tasks).

The Angular UI must have a dedicated "Manual Score" panel with:
- Article selector dropdown
- Task selector
- Large textarea for pasting raw LLM output
- "Score" button
- Results panel showing breakdown identical to the evaluation dashboard

---

## 9. Frontend — Angular Application Structure

```
frontend/
├── src/app/
│   ├── core/
│   │   ├── services/
│   │   │   ├── api.service.ts         (HTTP client wrapper)
│   │   │   ├── articles.service.ts
│   │   │   ├── dataset.service.ts
│   │   │   ├── runs.service.ts
│   │   │   └── scoring.service.ts
│   │   └── models/                    (TypeScript interfaces matching backend schemas)
│   ├── features/
│   │   ├── articles/
│   │   │   ├── article-list/          (upload CSV, table of all articles + status badges)
│   │   │   └── article-detail/        (full article + its DatasetItem side by side)
│   │   ├── dataset/
│   │   │   ├── dataset-overview/      (generation progress, stats)
│   │   │   └── dataset-item/          (per-article: all 4 tasks, reference outputs)
│   │   ├── runs/
│   │   │   ├── run-list/              (all runs, status, model names)
│   │   │   ├── run-create/            (form: model name, API key, base URL)
│   │   │   └── run-detail/            (per-run: progress bar, per-article scores table)
│   │   ├── evaluation/
│   │   │   ├── output-detail/         (one ModelOutput: all 4 task outputs + scores side-by-side)
│   │   │   └── model-comparison/      (multi-model score comparison charts)
│   │   ├── scoring/
│   │   │   └── manual-score/          (paste-and-score panel)
│   │   └── reports/
│   │       ├── executive-summary/     (markdown rendered report per run)
│   │       └── export/                (download JSON report)
│   └── shared/
│       ├── components/
│       │   ├── score-badge/           (colored chip for scores)
│       │   ├── progress-ring/         (circular progress)
│       │   ├── arabic-text/           (RTL text wrapper)
│       │   └── status-badge/
│       └── pipes/
│           └── arabic-date.pipe.ts
```

---

## 10. Dashboard Visualizations

Use **ngx-charts** or **Chart.js via ng2-charts** for all charts.

### 10.1 Overview Page
- **Processing pipeline bar**: 5 segments — Articles uploaded / Dataset generated /
  Models queued / Models completed / Reports generated — filled by count
- **Article status donut**: PENDING / GENERATING / READY / ERROR
- **Model comparison bar chart**: overall_score per model, sorted descending

### 10.2 Run Detail Page
- **Progress bar**: `processed_count / total_articles` with live polling (2s interval)
- **Score distribution histogram**: distribution of overall_score across all articles for this run
- **Per-task score radar chart**: NER / NLI / Summary / Cross-lingual scores for this model
- **Articles table**: sortable columns — article_id, title, ner_score, summary_score,
  nli_score, xling_score, overall_score, status. Clickable rows → output detail.

### 10.3 Model Comparison Page
- **Multi-model radar chart**: one series per model, axes = 4 task scores
- **Grouped bar chart**: per-task scores for all models side by side
- **Score heatmap**: rows = articles, columns = models, cell = overall_score
  (color scale green→red, articles sorted by difficulty)
- **Failure mode table**: articles where any model scored < 5.0 on any task

### 10.4 Output Detail Page (per article × model)
- Side-by-side panels: reference output | model output | score breakdown
- For NER: color-coded entity lists (green = correct, red = FP, orange = FN)
- For NLI: claim-by-claim table with predicted vs reference label
- For summary/xling: judge rubric breakdown as horizontal bar chart
- Raw JSON toggle for all outputs

### 10.5 Article Detail Page
- Original Arabic article (RTL, proper Arabic font)
- All 4 DatasetItem task inputs and reference outputs
- Scores from all evaluated models in a comparison table

---

## 11. Executive Summary Report Generation

**Trigger:** `POST /api/reports/generate/{run_id}`

**Prompt sent to JUDGE_MODEL:**
```
SYSTEM:
You are a senior NLP research lead writing an evaluation report.
Write in clear, professional English. Use markdown formatting.

USER:
Generate an executive summary report for the following Arabic LLM evaluation run.

Model evaluated: {model_name}
Total articles: {total_articles}
Articles successfully scored: {scored_count}

Aggregate scores:
  NER:            {avg_ner_score:.2f} / 10
  NLI:            {avg_nli_score:.2f} / 10
  Summarization:  {avg_summary_score:.2f} / 10
  Cross-lingual:  {avg_xling_score:.2f} / 10
  Overall:        {avg_overall_score:.2f} / 10

Score distribution:
  Articles scoring > 8.0: {high_count}
  Articles scoring 5.0–8.0: {mid_count}
  Articles scoring < 5.0: {low_count}

Most common judge feedback themes (from rubric reasoning fields):
{top_failure_themes}

Top 3 worst-performing articles:
{worst_articles}

Write a report with these sections:
## Overall Performance
## Strengths
## Weaknesses
## Task-by-Task Analysis
## Recommendations for Improvement
## Conclusion

Be specific. Reference actual scores. Identify patterns.
```

---

## 12. Real-Time Updates

Use **Server-Sent Events (SSE)** for live progress updates.

**Endpoint:** `GET /api/runs/{run_id}/stream`

Event types:
- `progress` — `{processed: int, total: int, current_article_id: str}`
- `article_scored` — `{article_id: str, overall_score: float}`
- `run_completed` — `{run_id: str, avg_score: float}`
- `error` — `{article_id: str, message: str}`

Angular service should subscribe to this SSE endpoint and update the run-detail
component state in real time.

---

## 13. Error Handling

- If any LLM call fails (timeout, rate limit, malformed JSON), log the error in
  `ModelOutput.error_message`, set status = ERROR, and continue to the next article.
  Do not abort the entire run.
- If JSON parsing fails for NER or NLI output, attempt to extract JSON from the
  response using a regex. If still fails, score that task as 0 and flag as parse error.
- All API keys must be stored encrypted in the database (use `cryptography.fernet`).
  Never return API keys in any API response — return masked strings only.
- Rate limiting: implement exponential backoff (1s, 2s, 4s, 8s) for all LLM calls.
  Max 3 retries per call.

---

## 14. Docker Compose Setup

Provide a `docker-compose.yml` that starts:
- `backend` — FastAPI on port 8000
- `worker` — Celery worker (same image as backend)
- `redis` — Redis 7 (broker + result backend)
- `frontend` — Angular served via nginx on port 4200

Include a `Makefile` with:
```
make dev        — start all services
make migrate    — run Alembic migrations
make seed       — insert sample data (5 articles) for dev/demo
make test       — run pytest backend tests
```

---

## 15. Acceptance Criteria

The system is complete when:

1. A CSV of 100 Arabic articles can be uploaded and parsed without errors
2. Clicking "Generate Dataset" produces 100 DatasetItems with all 4 tasks populated
3. A new evaluation run can be created by entering a model name and API key
4. The run executes asynchronously, with live progress visible in the dashboard
5. Each ModelOutput has scores for all 4 tasks
6. The manual scoring panel correctly scores a pasted NER JSON output against any article
7. The model comparison chart renders correctly for 2+ completed runs
8. The executive summary endpoint returns a structured markdown report
9. All Arabic text renders RTL with correct font in the Angular UI
10. The system handles a 429 rate-limit error from the LLM API gracefully
    (retries with backoff, does not crash the run)

---

## 16. Notes for the Implementing Developer

- Arabic text must always be rendered with `dir="rtl"` and font-family that includes
  a high-quality Arabic font. Use Google Fonts `Noto Naskh Arabic` or `Cairo`.
- All date fields in the API should be ISO 8601 strings.
- The SQLite database file should be at `/data/benchmark.db` and mounted as a volume.
- Do not hardcode any API keys anywhere in source code. All keys come from environment
  variables or the database config table.
- The Celery worker and FastAPI app share the same SQLAlchemy models — put models.py
  in a shared module imported by both.
- For the Angular project, use standalone components and Angular Material throughout.
  No NgModule-based architecture.
- All LLM calls must log: timestamp, model, prompt token count, completion token count,
  latency_ms, and whether the response parsed successfully. Store in a `llm_call_log`
  table for debugging.
