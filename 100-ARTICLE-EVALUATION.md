# 100-Article Arabic LLM Benchmark — Evaluation Results

## Overview

Full evaluation of 4 LLMs on Arabic NLP tasks using 100 Arabic articles across 5 categories (culture, finance, politics, sports, tech — 20 per category).

- **Teacher Model** (generates reference dataset): Claude Opus 4.6 (Anthropic)
- **Judge Model** (scores summaries & translations): GPT-5.2 (OpenAI)
- **Evaluation date**: April 2026
- **Articles**: 100 (sampled from 500-article corpus, seed=42, 20 per category)
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
| **DeepSeek Chat (V3)** | DeepSeek | API |
| **Mistral Large** | AWS Bedrock (`mistral.mistral-large-2402-v1:0`) | API |
| **Mueen AI** | Manual (browser-based) | Manual upload |

---

## Overall Results

| Model | NER | NLI | Summary | Translation | **Overall** |
|-------|:---:|:---:|:-------:|:-----------:|:-----------:|
| **Qwen 3.5 397B** | 7.54 | 9.89 | 9.08 | 9.26 | **8.62** |
| **DeepSeek Chat** | 7.12 | 9.88 | 8.70 | 8.86 | **8.38** |
| **Mistral Large** | 5.66 | 9.40 | 7.84 | 4.75 | **6.60** |
| **Mueen AI** | 3.92 | 7.36 | 7.10 | 5.45 | **5.79** |

### Ranking

1. **Qwen 3.5 397B** — 8.62 (best across all tasks)
2. **DeepSeek Chat** — 8.38 (strong second, near-perfect NLI)
3. **Mistral Large** — 6.60 (weak translation to Arabic: 4.75)
4. **Mueen AI** — 5.79 (lowest NER and NLI, competitive on finance)

---

## Per-Task Analysis

### NER (Named Entity Recognition) — Deterministic F1

| Model | Score | Notes |
|-------|:-----:|-------|
| Qwen 3.5 | **7.54** | Best entity extraction across Arabic text |
| DeepSeek | 7.12 | Close second |
| Mistral | 5.66 | Misses many entities |
| Mueen AI | 3.92 | Significant entity recognition gaps |

*Scoring: Weighted F1 (PERSON×0.35, LOCATION×0.25, ORG×0.25, MISC×0.15) with hallucination penalty.*

### NLI (Natural Language Inference) — Deterministic Weighted Accuracy

| Model | Score | Notes |
|-------|:-----:|-------|
| Qwen 3.5 | **9.89** | Near-perfect fact verification |
| DeepSeek | 9.88 | Essentially tied with Qwen |
| Mistral | 9.40 | Strong but occasional errors |
| Mueen AI | 7.36 | Weakest on claim classification |

*Scoring: Positional label matching with per-label weights (NOT_ENOUGH_INFO×1.5, REFUTED×1.2, SUPPORTED×1.0).*

### Summary (Arabic Summarization) — GPT-5.2 Judge

| Model | Score | Notes |
|-------|:-----:|-------|
| Qwen 3.5 | **9.08** | Excellent formal Arabic, strong coverage |
| DeepSeek | 8.70 | Good quality, occasional minor issues |
| Mistral | 7.84 | Decent but less consistent |
| Mueen AI | 7.10 | Acceptable but less grounded in source |

*Scoring: Judge rubric — factual accuracy (0-3), coverage (0-3), no added inference (0-2), register fluency (0-2), verbatim penalty (0-1).*

### Translation (English → Arabic) — GPT-5.2 Judge

| Model | Score | Notes |
|-------|:-----:|-------|
| Qwen 3.5 | **9.26** | Near-native Arabic translation quality |
| DeepSeek | 8.86 | Strong and faithful |
| Mueen AI | 5.45 | Partially faithful, some additions |
| Mistral | 4.75 | Struggles with Arabic generation |

*Scoring: Judge rubric — faithfulness (0-3), fluency (0-3), terminology (0-2), register (0-2).*

---

## Per-Category Breakdown

### Qwen 3.5 397B (Overall: 8.62)

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 20 | 7.42 | 10.00 | 9.54 | 9.11 | 8.81 |
| Finance | 23 | 8.57 | 9.72 | 9.10 | 9.22 | 8.91 |
| Politics | 23 | 7.03 | 9.75 | 9.04 | 9.51 | 8.51 |
| Sports | 15 | 7.69 | 10.00 | 8.81 | 9.09 | 8.53 |
| Tech | 23 | 6.97 | 10.00 | 8.91 | 9.33 | 8.48 |

### DeepSeek Chat (Overall: 8.38)

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 20 | 6.67 | 9.84 | 8.88 | 8.87 | 8.29 |
| Finance | 22 | 7.49 | 9.81 | 8.44 | 8.43 | 8.33 |
| Politics | 22 | 7.40 | 9.88 | 8.89 | 9.31 | 8.63 |
| Sports | 14 | 7.29 | 10.00 | 8.46 | 8.34 | 8.22 |
| Tech | 22 | 6.77 | 9.90 | 8.75 | 9.16 | 8.37 |

### Mistral Large (Overall: 6.60)

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 20 | 6.33 | 9.77 | 8.71 | 4.75 | 7.15 |
| Finance | 23 | 5.12 | 8.39 | 7.48 | 4.87 | 6.20 |
| Politics | 23 | 5.44 | 9.57 | 8.44 | 4.55 | 6.66 |
| Sports | 15 | 6.36 | 9.55 | 7.93 | 4.79 | 6.79 |
| Tech | 23 | 5.68 | 9.72 | 7.80 | 5.45 | 6.84 |

### Mueen AI (Overall: 5.79)

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 20 | 3.54 | 6.82 | 6.41 | 5.20 | 5.33 |
| Finance | 22 | 4.97 | 8.01 | 7.03 | 6.72 | 6.53 |
| Politics | 22 | 3.06 | 6.24 | 6.64 | 4.71 | 5.00 |
| Sports | 14 | 3.41 | 8.50 | 7.88 | 6.23 | 6.25 |
| Tech | 22 | 4.40 | 7.61 | 7.77 | 4.64 | 5.95 |

---

## Key Findings

1. **Qwen 3.5 is the clear winner** with 8.62 overall — the most consistent performer across all tasks and categories. Highest scores on NER (7.54), Summary (9.08), and Translation (9.26).

2. **DeepSeek Chat is a strong second** at 8.38 — virtually tied with Qwen on NLI (9.88 vs 9.89) and competitive on all other tasks. Best value for the speed/cost tradeoff.

3. **Mistral Large has a critical Arabic generation weakness** — scoring only 4.75 on translation (Eng→Arabic). Its NLI (9.40) and Summary (7.84) are decent, but the translation weakness drags its overall to 6.60.

4. **Mueen AI shows room for improvement** — weakest on NER (3.92) and NLI (7.36), but competitive on Finance articles (6.53 overall). The NLI gap may be partly due to claim text matching sensitivity.

5. **NLI is nearly saturated** — all API models score 9.3+ on fact verification. This task no longer discriminates well between strong models.

6. **Translation is the most discriminating task** — the spread from 4.75 (Mistral) to 9.26 (Qwen) is the widest, making it the best signal for Arabic language capability.

7. **Finance is the easiest category** for most models, while Politics tends to be harder (more nuanced claims, complex entity relationships).

---

## Methodology

### Dataset Generation
- 500 Arabic articles collected across 5 categories (100 each)
- 100 articles sampled (20 per category, `random.seed(42)`)
- Claude Opus 4.6 generated reference data via Anthropic Batch API (50% cost discount)
- 4 reference outputs per article: NER entities, 2-sentence Arabic summary, 4 NLI claims, English→Arabic translation pair

### Evaluation
- API models evaluated programmatically via their respective APIs
- Mueen AI evaluated manually via browser-based assistant with structured prompt
- Each model performed the same 4 tasks on the same 100 articles

### Scoring
- **NER**: Deterministic weighted F1 with Arabic normalization and hallucination penalty
- **NLI**: Deterministic positional label matching with per-label importance weights
- **Summary**: GPT-5.2 LLM-as-Judge with rubric (factual accuracy, coverage, inference, register, verbatim)
- **Translation**: GPT-5.2 LLM-as-Judge with rubric (faithfulness, fluency, terminology, register)
- **Overall**: Weighted average — NER×0.30 + NLI×0.20 + Summary×0.25 + Translation×0.25

### Infrastructure
- Backend: FastAPI + SQLite (Python 3.12)
- Frontend: Angular 20 + Material
- Multi-provider LLM client: OpenAI, Anthropic, AWS Bedrock, Dashscope, DeepSeek
- Anthropic Batch API for teacher generation (50% cost savings)
- 53 unit tests passing

---

## How to Reproduce

```bash
# 1. Start the platform
py -m uvicorn backend.main:app --port 8111
cd frontend && npx ng serve --port 4222

# 2. Upload articles
curl -X POST http://localhost:8111/api/articles/upload \
  -F "file=@arabic_500_dataset.json"

# 3. Sample 100 articles
py scripts/sample_100.py --seed 42 --per-category 20

# 4. Generate dataset + run evaluations
py scripts/run_benchmark.py --per-category 20 --seed 42

# 5. View results
# http://localhost:4222/comparison
# http://localhost:4222/runs
```
