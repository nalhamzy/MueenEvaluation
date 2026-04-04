# Full Pipeline Test Results

## Overview

This document records the results of running the complete Arabic LLM Benchmark pipeline end-to-end as a proof-of-concept with 3 articles, evaluating **2 student models**. **Test date: 2026-04-03.**

## Pipeline Steps

```
1. Upload 100 articles (JSON) ─► 100 articles in DB                    [PASS]
2. Generate dataset (3 articles) ─► Teacher LLM (GPT-4o) generates:    [PASS]
   - NER reference (named entities)
   - Summary reference (2-sentence Arabic فصحى)
   - NLI reference (4 claim-label pairs)
   - Coref reference (entity coreference spans)
3. Student evaluation (gpt-4o-mini) ─► Runs same 4 tasks per article   [PASS]
4. Deterministic scoring ─► NER F1, NLI weighted accuracy, Coref F1    [PASS]
5. LLM Judge scoring ─► Summary rubric evaluation                      [PASS]
6. Executive summary ─► AI-generated report                            [PASS]
```

## Test Configuration

| Setting | Value |
|---------|-------|
| Teacher Model | **Claude Opus 4.6** (Anthropic API) |
| Student Models | **gpt-4o-mini** (OpenAI), **Qwen3.5-397B-A17B** (Dashscope) |
| Judge Model | **GPT-5.2** (OpenAI) |
| Articles Evaluated | 3 |
| Tasks per Article | 4 (NER, Summary, NLI, Coref) |

### Multi-Provider Setup
The system uses 3 different LLM providers simultaneously:
- **Anthropic** (Claude Opus) — Teacher: generates reference dataset
- **OpenAI** (GPT-5.2) — Judge: scores summary quality
- **Alibaba Dashscope** (Qwen) — Student: evaluated via OpenAI-compatible API

## Dataset Generation Results (Claude Opus 4.6)

| Article | NER Entities | NLI Claims | Summary Length | Coref Spans |
|---------|-------------|------------|----------------|-------------|
| ART_001 | 7 | 4 (2S, 1R, 1N) | 883 chars | 28 |
| ART_002 | 18 | 4 (2S, 1R, 1N) | 1,199 chars | 45 |
| ART_003 | 18 | 4 (2S, 1R, 1N) | 925 chars | 35 |

Claude Opus produced significantly richer coreference data (28-45 spans per article) compared to GPT-4o.

## Cross-Model Comparison

```
Model                        NER    NLI  Summary   Coref  Overall
-----------------------------------------------------------------
gpt-4o-mini                 6.44  10.00     8.67    0.00     6.60
Qwen3.5-397B-A17B           7.55  10.00     8.28    0.27     6.89
                            -----  -----   -----   -----    -----
Winner:                     Qwen   TIE    gpt-4o   Qwen     Qwen
```

**Qwen3.5-397B-A17B wins overall** (6.89 vs 6.60) with stronger NER and the only non-zero coref score.

## Per-Article Scores: gpt-4o-mini

| Article | NER | NLI | Summary | Coref | Overall |
|---------|-----|-----|---------|-------|---------|
| ART_001 | 7.4 | 10.0 | 8.0 | 0.0 | 6.7 |
| ART_002 | 6.7 | 10.0 | 9.0 | 0.0 | 6.8 |
| ART_003 | 5.3 | 10.0 | 9.0 | 0.0 | 6.3 |
| **Average** | **6.44** | **10.00** | **8.67** | **0.00** | **6.60** |

## Per-Article Scores: Qwen3.5-397B-A17B

| Article | NER | NLI | Summary | Coref | Overall |
|---------|-----|-----|---------|-------|---------|
| ART_001 | 6.8 | 10.0 | 7.8 | 0.0 | 6.5 |
| ART_002 | 8.9 | 10.0 | 8.0 | 0.0 | 7.2 |
| ART_003 | 7.0 | 10.0 | 9.0 | 0.8 | 7.0 |
| **Average** | **7.55** | **10.00** | **8.28** | **0.27** | **6.89** |

### Score Weights
```
Overall = NER × 0.30 + NLI × 0.25 + Summary × 0.25 + Coref × 0.20
```

### Analysis

**NER**: Qwen (7.55) outperformed gpt-4o-mini (6.44) by +1.11 points. Qwen scored 8.9 on ART_002 (complex geopolitical article with many entities), showing strong Arabic entity extraction.

**NLI**: Both models achieved perfect 10.0 — all claims correctly classified as SUPPORTED/REFUTED/NOT_ENOUGH_INFO.

**Summary**: gpt-4o-mini (8.67) slightly edged Qwen (8.28). The GPT-5.2 judge noted Qwen occasionally added mild inferences not in the source.

**Coref**: Both scored near 0. Qwen got 0.8 on ART_003 (the only non-zero score), showing it can partially resolve coreference chains. This task remains the hardest — the reference data from Claude Opus is very detailed (28-45 spans) and the matching algorithm is strict.

## GPT-5.2 Judge Rubrics

### gpt-4o-mini

| Article | Factual (0-3) | Coverage (0-3) | No Inference (0-2) | Register (0-2) | Verbatim |
|---------|:---:|:---:|:---:|:---:|:---:|
| ART_001 | 3 | 2 | 1 | 2 | 0 |
| ART_002 | 3 | 2 | 2 | 2 | 0 |
| ART_003 | 3 | 2 | 2 | 2 | 0 |

### Qwen3.5-397B-A17B

| Article | Factual (0-3) | Coverage (0-3) | No Inference (0-2) | Register (0-2) | Verbatim |
|---------|:---:|:---:|:---:|:---:|:---:|
| ART_001 | 2 | 3 | 1 | 2 | 0 |
| ART_002 | 3 | 2 | 1 | 2 | 0 |
| ART_003 | 3 | 2 | 2 | 2 | 0 |

**Key differences**: GPT-5.2 as judge is stricter than GPT-4o was in the previous run. gpt-4o-mini got slightly better factual scores while Qwen got slightly better coverage on ART_001.
>
> ## Weaknesses
## Executive Summary Reports

Both runs generated 7,600+ character executive reports via GPT-5.2. Key findings from the reports:

**gpt-4o-mini**: "Strong summarization (8.67/10) and perfect NLI, but complete failure on coreference. Consistent mid-tier performance across all articles."

**Qwen3.5-397B-A17B**: "Reliably logically consistent (NLI 10.0) and generally produces good summaries (8.28/10). NER performance is good but inconsistent. Coreference remains a critical failure point."

## LLM Call Statistics

| Phase | Calls per Article | Total Calls (×2 runs) | Time |
|-------|-------------------|-----------------------|------|
| Teacher (Claude Opus) | 4 | 12 | ~30s total |
| Student (per model) | 4 | 12 per run | ~15-50s |
| Judge (GPT-5.2) | 1 | 3 per run | ~10s |
| Report (GPT-5.2) | - | 1 per run | ~10s |
| **Grand total** | | **~44 calls** | ~3 min |

Claude Opus as teacher was dramatically faster than GPT-4o (~10s vs ~90s per article).

## How to Reproduce

```bash
# 1. Start backend
py -m uvicorn backend.main:app --port 8001

# 2. Start frontend
cd frontend && npx ng serve --port 4200

# 3. Upload articles (via API or UI)
curl -X POST http://localhost:8001/api/articles/upload \
  -F "file=@aljazeera_arabic_news_dataset_100_articles.json"

# 4. Generate dataset (3 articles)
curl -X POST "http://localhost:8001/api/dataset/generate?limit=3"

# 5. Create evaluation run (via API or Runs page)
curl -X POST http://localhost:8001/api/runs \
  -H "Content-Type: application/json" \
  -d '{"model_name": "gpt-4o-mini"}'

# 6. Run LLM judge (after evaluation completes)
curl -X POST http://localhost:8001/api/scoring/judge-run/{run_id}

# 7. Generate executive summary
curl -X POST http://localhost:8001/api/reports/generate/{run_id}

# 8. View results
# - API: GET http://localhost:8001/api/runs/{run_id}/scores
# - UI:  http://localhost:4200/runs/{run_id}
```

## Test Suite Summary

| Test File | Tests | Status |
|-----------|-------|--------|
| test_articles.py | 8 | All pass |
| test_scoring.py | 19 | All pass |
| test_student_and_judge.py | 6 | All pass |
| test_full_pipeline.py | 1 | Integration test (requires API key) |
| **Total** | **34** | **33 unit + 1 integration** |
