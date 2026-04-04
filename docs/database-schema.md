# Database Schema

## Overview

SQLite database at `backend/data/benchmark.db`. Tables are auto-created by SQLAlchemy on startup via `Base.metadata.create_all()`.

## Entity Relationship Diagram

```
┌──────────────┐     1:1      ┌───────────────┐
│   Article    │─────────────►│  DatasetItem   │
│              │              │                │
│ id (PK)      │              │ article_id (FK)│
│ title        │              │ ner_reference  │
│ body         │              │ summary_ref    │
│ source       │              │ nli_claims     │
│ date         │              │ coref_ref      │
│ status       │              │ teacher_model  │
│ created_at   │              └───────┬────────┘
└──────┬───────┘                      │
       │                              │
       │ 1:N                          │ 1:N
       ▼                              ▼
┌──────────────┐     N:1      ┌───────────────┐
│ ModelOutput  │─────────────►│EvaluationRun   │
│              │              │                │
│ article_id   │              │ model_name     │
│ dataset_item │              │ status         │
│ run_id (FK)  │              │ total_articles │
│ ner_output   │              │ processed_count│
│ summary_out  │              └───────┬────────┘
│ nli_output   │                      │
│ coref_output │                      │ 1:N
│ *_score      │              ┌───────▼────────┐
│ overall_score│              │ExecutiveSummary │
└──────────────┘              │                │
                              │ run_id (FK)    │
                              │ content (md)   │
                              └────────────────┘

┌──────────────┐
│ LLMCallLog   │  (standalone, no FK relationships)
│              │
│ model        │
│ prompt_tokens│
│ latency_ms   │
│ success      │
│ task_type    │
└──────────────┘
```

## Tables

### `articles`
Primary entity. One row per uploaded news article.

### `dataset_items`
One-to-one with `articles`. Contains teacher-generated reference data for all 4 NLP tasks. Created during dataset generation phase.

### `evaluation_runs`
One row per model evaluation attempt. Tracks progress and status.

### `model_outputs`
The join table between runs and dataset items. One row per (article × model) combination. Stores both raw LLM outputs and computed scores.

### `executive_summaries`
AI-generated reports. FK to `evaluation_runs` (nullable for cross-model comparisons).

### `llm_call_logs`
Debugging table. Every LLM API call is logged with latency, token counts, and success/failure status. No foreign keys — purely observational.

## SQLAlchemy Notes

- Models defined in `backend/models.py`
- Uses SQLAlchemy 2.0 `Mapped` annotation style
- JSON columns store Python `dict`/`list` natively (SQLite JSON1 extension)
- UUIDs stored as strings (SQLite has no native UUID type)
- `datetime.utcnow()` used for timestamps (will migrate to `datetime.now(UTC)` in future)
