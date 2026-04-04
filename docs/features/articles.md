# Articles Feature

## Overview

The Articles feature handles ingesting Arabic news articles from CSV or JSON files, storing them in SQLite, and exposing CRUD endpoints for the frontend.

## Data Flow

```
Upload File ──► csv_service.py ──► Parse + Validate ──► Insert to DB ──► Return stats
                  │                                          │
                  ├── JSON: json.loads → list[dict]          │
                  └── CSV: csv.DictReader → list[dict]       │
                                                             ▼
                                                    Article (status=PENDING)
```

## Data Model

**Table: `articles`**

| Column | Type | Description |
|--------|------|-------------|
| `id` | String PK | Format: `ART_001`, `ART_002`, etc. |
| `title` | Text | Article headline (Arabic, UTF-8) |
| `body` | Text | Full article text (Arabic, UTF-8) |
| `source` | String | Publication name (e.g., "aljazeera") |
| `date` | Date | Publication date |
| `status` | Enum | `PENDING` → `GENERATING` → `READY` \| `ERROR` |
| `created_at` | DateTime | Row insertion timestamp |

### Status Lifecycle

```
PENDING ──► GENERATING ──► READY
                │
                └──► ERROR
```

- **PENDING**: Article uploaded, awaiting dataset generation
- **GENERATING**: Teacher LLM is currently processing this article
- **READY**: All 4 dataset tasks have been generated successfully
- **ERROR**: LLM call failed after retries

## API Endpoints

### `POST /api/articles/upload`

Accepts a multipart file upload (`.json` or `.csv`).

**JSON format** (matches the Al Jazeera dataset):
```json
[
  {
    "id": 1,
    "title": "عنوان المقال",
    "body": "نص المقال الكامل...",
    "source": "aljazeera",
    "date_published": "2026-03-14T16:12:42Z"
  }
]
```

**CSV format**:
```csv
article_id,title,body,source,date
ART_001,عنوان أول,نص المقال,aljazeera,2026-03-14
```

**Response**:
```json
{
  "total": 100,
  "inserted": 100,
  "skipped": 0,
  "errors": []
}
```

**Behavior**:
- Deduplicates by `article_id` — re-uploading the same file skips existing articles
- Validates that `title` and `body` are non-empty
- Auto-detects format by file extension; falls back to JSON-first if ambiguous

### `GET /api/articles`

Returns paginated list. Query params: `skip` (default 0), `limit` (default 100).

### `GET /api/articles/{article_id}`

Returns single article. 404 if not found.

## Implementation Details

### File: `backend/services/csv_service.py`

Key design decisions:

1. **Dual format support**: The real dataset is JSON (Al Jazeera scrape), but the spec requests CSV support. Both are implemented with a shared `_insert_articles()` function.

2. **Field mapping**: The JSON dataset uses `id` (int) and `date_published` (ISO 8601 with time), while the spec CSV uses `article_id` (string) and `date` (date only). The service normalizes both.

3. **ID normalization**: Integer IDs are zero-padded to `ART_001` format for consistency.

4. **Date parsing**: Handles both ISO 8601 with timezone (`2026-03-14T16:12:42Z`) and plain dates (`2026-03-14`).

### Error Handling

- Missing `title` or `body` → row skipped, error logged in response
- Duplicate `article_id` → row skipped silently (counted as `skipped`)
- Invalid date → stored as `NULL` (article still inserted)

## Testing

```bash
py -m pytest backend/tests/test_articles.py -v
```

Tests cover:
- JSON upload (happy path)
- CSV upload (happy path)
- Deduplication on re-upload
- List with pagination
- Get by ID
- 404 for missing article
- Validation (missing body)
