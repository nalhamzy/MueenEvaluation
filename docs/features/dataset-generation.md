# Dataset Generation (Teacher Service)

## Overview

The Teacher service uses an LLM (default: GPT-4o) to generate a structured evaluation dataset from uploaded Arabic articles. Each article produces exactly one `DatasetItem` containing reference outputs for 4 NLP tasks.

## Tasks Generated

| Task | Output Type | Field | Description |
|------|-------------|-------|-------------|
| **NER** | JSON | `ner_reference` | Named entities: PERSON, LOCATION, ORGANIZATION, MISC |
| **Summary** | Text | `summary_reference` | 2-sentence formal Arabic (فصحى) summary |
| **NLI** | JSON | `nli_claims` | 4 claim-label pairs (2 SUPPORTED, 1 REFUTED, 1 NOT_ENOUGH_INFO) |
| **Coreference** | JSON | `coref_reference` | Entity coreference resolution — JSON array of {span, referent, paragraph} |

## Data Model

**Table: `dataset_items`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID PK | Auto-generated |
| `article_id` | FK → articles | One-to-one relationship |
| `ner_input` | Text | Article body used as NER input |
| `ner_reference` | JSON | `{"PERSON":[], "LOCATION":[], "ORGANIZATION":[], "MISC":[]}` |
| `summary_input` | Text | Full article body |
| `summary_reference` | Text | 2-sentence فصحى reference summary |
| `nli_input` | Text | Article body |
| `nli_claims` | JSON | `[{"claim": str, "label": str}, ...]` |
| `coref_input` | Text | Article body |
| `coref_reference` | JSON | `[{"span": str, "referent": str, "paragraph": int}, ...]` |
| `generated_at` | DateTime | When generation completed |
| `teacher_model` | String | Model used (e.g., "gpt-4o") |

## Architecture

```
POST /api/dataset/generate?limit=3
         │
         ▼
    BackgroundTask
         │
         ▼
generate_dataset_task(limit=3)
    ├── Query PENDING articles (with optional limit)
    └── For each article:
            ├── Set status → GENERATING
            ├── Call LLM × 4 (NER, Summary, NLI, Coref)
            ├── Parse JSON responses
            ├── Create/update DatasetItem
            ├── Set status → READY
            └── On error: Set status → ERROR, continue to next
```

## Prompt Engineering

Each task has a carefully designed system + user prompt pair. Key design principles:

1. **JSON-only output**: NER and NLI prompts instruct the model to return raw JSON with no markdown fences, no preamble. `json_mode=True` is set for these calls.

2. **Explicit constraints**: Each prompt includes numbered "Hard rules" to prevent common failure modes (e.g., hallucinated entities, verbatim copying, obvious fabrications).

3. **Arabic-specific rules**: Summary prompt enforces formal MSA (فصحى), NER prompt handles definite article (ال) deduplication, NLI requires Arabic claims.

### Prompt Locations

All prompts are defined as constants in `backend/services/teacher_service.py`:
- `NER_SYSTEM` / `NER_USER`
- `SUMMARY_SYSTEM` / `SUMMARY_USER`
- `NLI_SYSTEM` / `NLI_USER`
- `COREF_SYSTEM` / `COREF_USER`

## LLM Client

See [LLM Integration](../llm-integration.md) for the shared client with retry logic.

## API Endpoints

### `POST /api/dataset/generate?limit=N`

Triggers background generation. Optional `limit` parameter for POC testing.

### `GET /api/dataset`

List all DatasetItems with pagination.

### `GET /api/dataset/{article_id}`

Get DatasetItem for a specific article.

### `GET /api/dataset/stats`

Returns counts: `total_items`, `completed`, `pending`.

## Error Handling

- **LLM call failure**: Article status set to ERROR, generation continues for remaining articles
- **JSON parse failure**: `parse_json_response()` strips markdown fences before parsing; raises on total failure
- **Rate limiting**: Exponential backoff (1s → 2s → 4s), max 3 retries per call

## Testing

```bash
# Unit tests (no LLM calls)
py -m pytest backend/tests/test_articles.py -v

# POC test with real LLM calls (3 articles)
py -m pytest backend/tests/test_teacher_poc.py -v -s
```

The POC test verifies:
- All 4 tasks generate valid output
- NER has the expected 4 categories
- NLI has ≥3 claims with correct labels
- Summary is a non-empty string
- Coref is a valid JSON array with span/referent/paragraph keys
- Article status transitions to READY
