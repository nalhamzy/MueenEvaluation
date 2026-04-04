# API Reference

Base URL: `http://localhost:8000`

## Health Check

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Returns `{"status": "ok"}` |

## Articles

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/articles/upload` | Upload CSV/JSON file (multipart) |
| GET | `/api/articles` | List all articles (`?skip=0&limit=100`) |
| GET | `/api/articles/{id}` | Get single article |

### Upload Response
```json
{"total": 100, "inserted": 100, "skipped": 0, "errors": []}
```

## Dataset

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/dataset/generate?limit=N` | Trigger teacher generation (optional limit) |
| GET | `/api/dataset` | List all DatasetItems |
| GET | `/api/dataset/stats` | `{total_items, completed, pending}` |
| GET | `/api/dataset/{article_id}` | DatasetItem for specific article |

## Evaluation Runs

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/runs` | Create run `{model_name, api_key?, base_url?}` |
| GET | `/api/runs` | List all runs |
| GET | `/api/runs/{id}` | Single run detail |
| DELETE | `/api/runs/{id}` | Cancel queued/running run |

## Outputs

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/outputs/{run_id}` | All outputs for a run |
| GET | `/api/outputs/{run_id}/{article_id}` | Single output detail |

## Scoring

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/scoring/score-output?output_id=X` | Score one ModelOutput |
| POST | `/api/scoring/score-run/{run_id}` | Score entire run |
| POST | `/api/scoring/score-manual` | Manual paste-and-score |

### Manual Score Request
```json
{
  "article_id": "ART_001",
  "task": "ner | summary | nli | coref",
  "model_output": "raw JSON string or text"
}
```

## Reports

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/reports/summary/{run_id}` | Get executive summary |
| POST | `/api/reports/generate/{run_id}` | Generate/regenerate summary |
| GET | `/api/reports/comparison` | Cross-model comparison stats |
| GET | `/api/reports/export/{run_id}` | Download full JSON report |

## Config

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/config` | Current config (keys masked) |
| PUT | `/api/config` | Update config |

### Config Response
```json
{
  "teacher_model": "gpt-4o",
  "judge_model": "gpt-4o",
  "student_models": "gpt-4o-mini",
  "openai_base_url": null,
  "teacher_api_key": "sk-proj-...6QSb",
  "student_api_key": "sk-proj-...6QSb",
  "judge_api_key": "sk-proj-...6QSb"
}
```
