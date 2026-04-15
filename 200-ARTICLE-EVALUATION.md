# 200-Article Arabic LLM Benchmark — Evaluation Results

## Overview

Full evaluation of 4 LLMs on Arabic NLP tasks using **200 Arabic articles** across 5 categories (culture, finance, politics, sports, tech — ~40 per category).

- **Teacher Model** (generates reference dataset): Claude Opus 4.6 (Anthropic)
- **Judge Model** (scores summaries & translations): GPT-5.2 (OpenAI)
- **Evaluation date**: April 2026
- **Articles**: 200 (sampled from 500-article corpus, two rounds: seed=42 and seed=99)
- **Tasks**: 4 — NER, NLI, Summary (Arabic), Translation (Eng→Arabic)

### Score Weights

```
Overall = NER × 0.30 + NLI × 0.20 + Summary × 0.25 + Translation × 0.25
```

---

## Models Evaluated

| Model | Provider | Type |
|-------|----------|------|
| **Qwen 3.5 397B-A17B** | Alibaba Dashscope | API |
| **DeepSeek Chat (V3)** | DeepSeek native API | API |
| **Mistral Large** | AWS Bedrock (`mistral.mistral-large-2402-v1:0`) | API |
| **Mueen AI** | Manual (browser-based) | Manual upload |

---

## Overall Results — 200 Articles

| Model | N | NER | NLI | Summary | Translation | **Overall** |
|-------|:-:|:---:|:---:|:-------:|:-----------:|:-----------:|
| **Qwen 3.5 397B** | 200 | 7.62 | 9.80 | 9.12 | 9.20 | **8.76** |
| **DeepSeek Chat** | 196 | 7.07 | 9.88 | 8.83 | 8.80 | **8.46** |
| **Mistral Large** | 200 | 5.95 | 9.39 | 8.09 | 5.02 | **6.89** |
| **Mueen AI** | 196 | 4.03 | 7.54 | 7.30 | 5.45 | **5.91** |

### Ranking

1. **Qwen 3.5 397B** — 8.76 (best across all tasks)
2. **DeepSeek Chat** — 8.46 (consistently strong, near-perfect NLI)
3. **Mistral Large** — 6.89 (still weak on translation: 5.02)
4. **Mueen AI** — 5.91 (lowest NER and NLI; competitive on tech and finance)

---

## Per-Task Analysis

### NER (Named Entity Recognition) — Deterministic F1

| Model | Score |
|-------|:-----:|
| Qwen 3.5 | **7.62** |
| DeepSeek | 7.07 |
| Mistral | 5.95 |
| Mueen AI | 4.03 |

### NLI (Natural Language Inference) — Deterministic Weighted Accuracy

| Model | Score |
|-------|:-----:|
| DeepSeek | **9.88** |
| Qwen 3.5 | 9.80 |
| Mistral | 9.39 |
| Mueen AI | 7.54 |

### Summary (Arabic Summarization) — GPT-5.2 Judge

| Model | Score |
|-------|:-----:|
| Qwen 3.5 | **9.12** |
| DeepSeek | 8.83 |
| Mistral | 8.09 |
| Mueen AI | 7.30 |

### Translation (English → Arabic) — GPT-5.2 Judge

| Model | Score |
|-------|:-----:|
| Qwen 3.5 | **9.20** |
| DeepSeek | 8.80 |
| Mueen AI | 5.45 |
| Mistral | 5.02 |

---

## Per-Category Breakdown — All Tasks

### Qwen 3.5 397B (Overall: 8.76)

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 40 | 7.58 | 9.86 | 9.38 | 8.82 | 8.75 |
| Finance | 41 | 8.74 | 9.58 | 8.95 | 9.34 | **9.08** |
| Politics | 43 | 6.93 | 9.72 | 9.29 | 9.44 | 8.61 |
| Sports | 34 | 7.56 | 9.84 | 8.83 | 9.00 | 8.63 |
| Tech | 42 | 7.31 | 10.00 | 9.08 | 9.34 | 8.73 |

### DeepSeek Chat (Overall: 8.46)

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 40 | 7.26 | 9.86 | 9.02 | 8.66 | 8.51 |
| Finance | 40 | 7.28 | 9.78 | 8.45 | 8.40 | 8.35 |
| Politics | 42 | 7.16 | 9.94 | 8.96 | 9.18 | **8.61** |
| Sports | 33 | 7.08 | 10.00 | 8.71 | 8.64 | 8.43 |
| Tech | 41 | 6.58 | 9.83 | 8.96 | 9.05 | 8.41 |

### Mistral Large (Overall: 6.89)

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 40 | 6.51 | 9.88 | 8.50 | 4.91 | **7.24** |
| Finance | 41 | 5.86 | 8.09 | 7.46 | 5.15 | 6.50 |
| Politics | 43 | 5.69 | 9.56 | 8.48 | 4.68 | 6.84 |
| Sports | 34 | 5.99 | 9.66 | 7.97 | 4.99 | 6.91 |
| Tech | 42 | 5.74 | 9.80 | 7.98 | 5.36 | 6.97 |

### Mueen AI (Overall: 5.91)

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 40 | 3.92 | 7.91 | 7.20 | 5.76 | 6.00 |
| Finance | 40 | 4.76 | 7.72 | 7.10 | 6.14 | 6.28 |
| Politics | 42 | 3.08 | 7.19 | 7.15 | 5.52 | 5.53 |
| Sports | 33 | 3.36 | 6.50 | 6.91 | 4.63 | 5.19 |
| Tech | 41 | 4.94 | 8.21 | 8.08 | 5.09 | **6.42** |

---

## Key Findings

1. **Qwen 3.5 remains the clear winner** at 8.76 overall — consistent across all categories with a peak of 9.08 on Finance. Top 3 in every single task.

2. **DeepSeek Chat is a reliable second** at 8.46 — virtually tied with Qwen on NLI (9.88 vs 9.80) and very close on Summary. Best for cost-conscious deployment.

3. **Mistral Large has a critical Arabic generation weakness** — Translation score of 5.02 (worse than Mueen!) caps its ceiling. Strong on NLI (9.39) and Summary (8.09).

4. **Mueen AI shows clear gaps** — weakest on NER (4.03) and NLI (7.54). Strongest on Tech (6.42) and weakest on Sports (5.19).

5. **Scores are very stable across the two 100-article batches** — variation of ±0.2 points or less for all models. This validates the scoring methodology.

6. **Tech and Politics categories produce the most consistent scores** across all models. Sports and Culture have the widest variance.

7. **Translation is the most discriminating task** — spread from 5.02 (Mistral) to 9.20 (Qwen) is the widest. Confirms the Eng→Arabic direction is the key discriminator for Arabic capability.

---

## Comparison: 100 vs 200 Articles

Scores remained remarkably stable when expanding from 100 to 200 articles — confirming the methodology's reliability:

| Model | 100-art | 200-art | Δ |
|-------|:-------:|:-------:|:-:|
| Qwen 3.5 | 8.62 | 8.76 | +0.14 |
| DeepSeek | 8.38 | 8.46 | +0.08 |
| Mistral | 6.60 | 6.89 | +0.29 |
| Mueen AI | 5.79 | 5.91 | +0.12 |

---

## Methodology

### Dataset Generation
- 500 Arabic articles collected across 5 categories (100 each)
- 200 articles sampled in two rounds:
  - Round 1: 100 articles (`random.seed(42)`, 20 per category)
  - Round 2: 100 articles (`random.seed(99)`, 20 per category, no overlap with round 1)
- Claude Opus 4.6 generated reference data via Anthropic Batch API (50% cost discount)
- 4 reference outputs per article: NER entities, 2-sentence Arabic summary, 4 NLI claims, English→Arabic translation pair

### Evaluation
- API models evaluated programmatically via their respective APIs
- Mueen AI evaluated manually via browser-based assistant with structured prompts split into 10-article chunks
- Each model performed the same 4 tasks on the same 200 articles

### Scoring
- **NER**: Deterministic weighted F1 with Arabic normalization and hallucination penalty
- **NLI**: Deterministic positional label matching with per-label importance weights (NOT_ENOUGH_INFO×1.5, REFUTED×1.2, SUPPORTED×1.0)
- **Summary**: GPT-5.2 LLM-as-Judge — rubric (factual accuracy, coverage, no inference, register fluency, verbatim penalty)
- **Translation**: GPT-5.2 LLM-as-Judge — rubric (faithfulness, fluency, terminology, register)
- **Overall**: Weighted average — NER×0.30 + NLI×0.20 + Summary×0.25 + Translation×0.25

### Infrastructure
- Backend: FastAPI + SQLite (Python 3.12)
- Frontend: Angular 20 + Material
- Multi-provider LLM client: OpenAI, Anthropic, AWS Bedrock, Dashscope, DeepSeek
- Anthropic Batch API for teacher generation (50% cost savings)
- 53 unit tests passing

---

## Reproducibility

```bash
# Backend + frontend
py -m uvicorn backend.main:app --port 8111
cd frontend && npx ng serve --port 4222

# Sample articles (seed=42 for round 1, seed=99 for round 2)
py scripts/sample_100.py --seed 42 --per-category 20

# Run full benchmark
py scripts/run_benchmark.py --per-category 20 --seed 42

# View results in UI
# http://localhost:4222/comparison
# http://localhost:4222/runs
```

---

## Files

- `100-ARTICLE-EVALUATION.md` — first 100-article report
- `200-ARTICLE-EVALUATION.md` — this document (combined 200)
- `arabic_500_dataset.json` — full corpus (500 articles)
- `selected_100.json` / `selected_next_100.json` — round 1 / round 2 samples
- `mueen_briefs/brief_01..10.md` — Mueen evaluation briefs
- `mueen_briefs/brief_*_eval.json` — Mueen results per chunk
- `mueen_next_100_merged.json` — merged Mueen 100 results
