# Arabic LLM Benchmark Platform — Developer Guide

## Architecture Overview

```
┌─────────────┐     HTTP/JSON      ┌─────────────────┐     SQLite
│   Angular    │ ◄───────────────► │   FastAPI        │ ◄──────────► benchmark.db
│   Frontend   │     Port 4200     │   Backend        │     Port 8000
└─────────────┘                    └────────┬────────┘
                                            │
                                   ┌────────▼────────┐
                                   │  OpenAI-compat   │
                                   │  LLM APIs        │
                                   └─────────────────┘
```

### Processing Pipeline

```
1. Upload CSV/JSON ──► 2. Generate Dataset (Teacher LLM) ──► 3. Run Evaluation (Student LLM)
                                                                        │
4. Score Outputs (Deterministic + LLM Judge) ◄──────────────────────────┘
        │
        ▼
5. Executive Summary Report
```

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
ng serve --port 4200
```

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `backend/` | FastAPI application, models, services, tests |
| `frontend/` | Angular 20 application with Material UI |
| `docs/` | Developer documentation (this directory) |

## Documentation Index

| Document | Description |
|----------|-------------|
| [Articles Feature](./features/articles.md) | CSV/JSON ingestion, CRUD, data model |
| [Dataset Generation](./features/dataset-generation.md) | Teacher LLM prompts, pipeline, error handling |
| [Scoring Service](./features/scoring.md) | NER F1, NLI weighted, Coref F1, LLM judge (summary) |
| [Frontend](./features/frontend.md) | Angular app, components, routing, Arabic text |
| [API Reference](./api-reference.md) | All endpoints, request/response schemas |
| [Database Schema](./database-schema.md) | Tables, relationships, migrations |
| [LLM Integration](./llm-integration.md) | Client abstraction, retry logic, logging |

## Environment Variables

See `.env.example` for all required variables. Keys are loaded via `pydantic-settings` in `backend/config.py`.
