# LLM Integration

## Overview

All LLM calls go through a shared client in `backend/services/llm_client.py`. This provides:
- OpenAI-compatible API calls (works with GPT, Claude via proxy, Mistral, etc.)
- Exponential backoff retry (1s → 2s → 4s, max 3 attempts)
- Structured call logging to `llm_call_logs` table
- JSON response parsing with markdown fence stripping

## Client API

```python
from services.llm_client import call_llm, parse_json_response

# Text response
text = call_llm(
    api_key="sk-...",
    model="gpt-4o",
    system_prompt="You are a helpful assistant.",
    user_prompt="Summarize this article...",
    db=db_session,         # optional: enables call logging
    task_type="teacher_summary",  # logged for debugging
)

# JSON response (sets response_format=json_object)
json_text = call_llm(
    api_key="sk-...",
    model="gpt-4o",
    system_prompt="Return valid JSON only.",
    user_prompt="Extract entities...",
    json_mode=True,
    db=db_session,
    task_type="teacher_ner",
)
data = parse_json_response(json_text)
```

## Retry Logic

```
Attempt 1 ──► Success → return
         └──► Failure → sleep 1s
Attempt 2 ──► Success → return
         └──► Failure → sleep 2s
Attempt 3 ──► Success → return
         └──► Failure → raise last exception
```

Handles all exception types: network errors, rate limits (429), server errors (500+), timeouts.

## Call Logging

Every LLM call (success or failure) is logged to the `llm_call_logs` table:

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Auto-generated |
| `timestamp` | DateTime | When the call was made |
| `model` | String | Model identifier (e.g., "gpt-4o") |
| `prompt_tokens` | Integer | Input token count (from API response) |
| `completion_tokens` | Integer | Output token count |
| `latency_ms` | Integer | Wall-clock time in milliseconds |
| `success` | Boolean | Whether the call succeeded |
| `error_message` | Text | Error details if failed |
| `task_type` | String | e.g., "teacher_ner", "student_summary", "judge_summary" |

## JSON Parsing

`parse_json_response(text)` handles common LLM output quirks:
1. Strips leading/trailing whitespace
2. Removes markdown code fences (` ```json ... ``` `)
3. Parses with `json.loads()`

## Configuration

LLM configuration is managed in `backend/config.py` via environment variables:

```
TEACHER_MODEL=gpt-4o          # Model for dataset generation
TEACHER_API_KEY=               # Falls back to OPENAI_API_KEY
JUDGE_MODEL=gpt-4o             # Model for scoring (LLM-as-Judge)
JUDGE_API_KEY=                  # Falls back to OPENAI_API_KEY
STUDENT_MODELS=gpt-4o-mini     # Comma-separated list of models to evaluate
STUDENT_API_KEY=                # Falls back to OPENAI_API_KEY
OPENAI_BASE_URL=               # Override for non-OpenAI endpoints
OPENAI_API_KEY=sk-...          # Default API key
```

Keys are resolved with fallback: specific key → `OPENAI_API_KEY`.

## Security

- API keys are **never** returned in API responses — `GET /api/config` returns masked strings
- Keys are loaded from environment variables via `pydantic-settings`
- The `.env` file should be in `.gitignore`
