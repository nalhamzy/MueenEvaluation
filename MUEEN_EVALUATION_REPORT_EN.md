# Mueen AI — Comprehensive Evaluation Report

**Date:** April 2026
**Evaluation framework:** Arabic LLM Benchmark Platform
**Articles evaluated:** 200 Arabic articles across 5 domains
**Models compared:** Mueen AI vs Qwen 3.5 397B, DeepSeek Chat (V3), Mistral Large

---

## 1. Executive Summary

Mueen AI was evaluated on **200 Arabic news articles** across 5 categories (culture, finance, politics, sports, tech) on **4 NLP tasks**: Named Entity Recognition (NER), Natural Language Inference (NLI), Arabic Summarization, and English-to-Arabic Translation. Three commercial frontier models were evaluated on the same dataset for comparison.

### Headline result

Mueen AI achieved an **overall score of 5.91 / 10**, placing it in **4th position** among the 4 evaluated models. The leading frontier model (Qwen 3.5 397B) scored 8.76/10, a gap of **2.85 points**.

### Final leaderboard (200 articles)

| Rank | Model | NER | NLI | Summary | Translation | **Overall** |
|:----:|-------|:---:|:---:|:-------:|:-----------:|:-----------:|
| 1 | **Qwen 3.5 397B** | 7.62 | 9.80 | 9.12 | 9.20 | **8.76** |
| 2 | DeepSeek Chat | 7.07 | 9.88 | 8.83 | 8.80 | **8.46** |
| 3 | Mistral Large | 5.95 | 9.39 | 8.09 | 5.02 | **6.89** |
| 4 | **Mueen AI** | 4.03 | 7.54 | 7.30 | 5.45 | **5.91** |

### Key insight

Mueen AI's relative weakness is concentrated in **Named Entity Recognition** (4.03/10, vs 7.62 for the leader). NLI also shows a meaningful gap (7.54 vs 9.80). Generative tasks (Summary 7.30, Translation 5.45) are closer to the field — actually outperforming Mistral Large on Translation (5.45 vs 5.02).

---

## 2. Methodology

### Architecture

```
                Article (Arabic)
                       │
                       ▼
          ┌────────────────────────┐
          │  Teacher: Claude Opus  │  generates reference outputs
          │       (4 tasks)        │
          └────────────┬───────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │   Student: 4 models    │  produces predictions
          │   (Mueen + 3 others)   │
          └────────────┬───────────┘
                       │
                       ▼
       ┌────────────────────────────────┐
       │ Scoring                        │
       │   NER, NLI: deterministic F1   │
       │   Summary, Translation: judge  │
       │   Judge model: GPT-5.2         │
       └────────────────────────────────┘
```

### The 4 tasks

1. **NER (Named Entity Recognition)** — Extract entities into 4 categories (PERSON, LOCATION, ORGANIZATION, MISC) from each Arabic article. Scored deterministically using weighted F1 with Arabic normalization (diacritics, alef variants, definite article ال) and a hallucination penalty for entities not found in the source.

2. **NLI (Natural Language Inference / Fact Verification)** — Given an article and 4 claims, label each as `SUPPORTED`, `REFUTED`, or `NOT_ENOUGH_INFO`. Scored by positional weighted accuracy (NOT_ENOUGH_INFO×1.5, REFUTED×1.2, SUPPORTED×1.0).

3. **Arabic Summarization** — Produce a 2-sentence summary in formal Modern Standard Arabic (فصحى). Scored by GPT-5.2 with a 5-criterion rubric: factual accuracy (0–3), coverage (0–3), no added inference (0–2), register fluency (0–2), and verbatim copying penalty (0–1).

4. **English→Arabic Translation** — Translate a 3-sentence English summary of the article into formal Arabic. Scored by GPT-5.2 with a 4-criterion rubric: faithfulness (0–3), fluency (0–3), terminology handling (0–2), register/formality (0–2).

### Overall score formula

```
Overall = NER × 0.30 + NLI × 0.20 + Summary × 0.25 + Translation × 0.25
```

### Dataset

- 500 Arabic articles collected across 5 categories (100 each)
- 200 articles sampled for evaluation: round 1 (seed=42), round 2 (seed=99)
- ~40 articles per category in the final 200-article evaluation set

---

## 3. Detailed Results

### Per-task scores (all 4 models)

| Task | Qwen 3.5 | DeepSeek | Mistral | Mueen AI | Mueen Rank |
|------|:--------:|:--------:|:-------:|:--------:|:----------:|
| **NER** | 7.62 | 7.07 | 5.95 | **4.03** | 4 |
| **NLI** | 9.80 | 9.88 | 9.39 | **7.54** | 4 |
| **Summary** | 9.12 | 8.83 | 8.09 | **7.30** | 4 |
| **Translation** | 9.20 | 8.80 | 5.02 | **5.45** | 3 |
| **Overall** | 8.76 | 8.46 | 6.89 | **5.91** | 4 |

Note: On Translation, Mueen AI outperforms Mistral Large.

### Mueen AI per-category breakdown

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 40 | 3.92 | 7.91 | 7.20 | 5.76 | **6.00** |
| Finance | 40 | 4.76 | 7.72 | 7.10 | 6.14 | **6.28** |
| Politics | 42 | 3.08 | 7.19 | 7.15 | 5.52 | **5.53** |
| Sports | 33 | 3.36 | 6.50 | 6.91 | 4.63 | **5.19** |
| Tech | 41 | 4.94 | 8.21 | 8.08 | 5.09 | **6.42** |

---

## 4. Mueen AI Deep-Dive

### Strengths

- **Best category: Tech** with overall score 6.42/10. Mueen handles tech content with the most consistency.
- **Second-best category: Finance** (6.28/10).
- **Translation is Mueen's relatively strongest task** ranked against the field — 3rd of 4 models, beating Mistral Large.
- **NLI labels are usable** when claims are presented in the expected format (7.54/10) — meaningful signal, even if behind the leaders.

### Weaknesses

- **Worst category: Sports** with overall score 5.19/10. The sports domain produces the most misses.
- **NER (4.03/10) is the weakest task overall** — the gap to the leader (Qwen 3.5: 7.62) is 3.59 points. Mueen frequently misses entities that the reference includes, particularly people's full names and organization variants.
- **NLI accuracy (7.54/10) trails the field** — all three commercial models cluster at 9.4–9.9 on this task.

### Worked examples

Five articles (one per category, picked at the per-category median Mueen score) are reproduced in the companion file `mueen_evaluation_samples.md`. Each example shows Mueen's actual outputs side-by-side with the Claude Opus reference and the GPT-5.2 judge feedback.

---

## 5. Failure Pattern Analysis

Patterns observed across the 196 scored Mueen articles:

1. **NER under-extraction** — Mueen tends to extract a smaller entity set than the reference. The reference includes morphological variants and secondary mentions; Mueen tends to capture only the most prominent.

2. **NLI claim-text drift** — In the first manual round, Mueen rewrote several claims rather than copying them verbatim. Once the prompt was tightened to enforce verbatim claim copying, NLI scores rose substantially (2.90 → 7.36 on the same articles). This is a prompt-engineering finding, not a model capability finding.

3. **Summary register** — Summaries are in MSA but tend to be more verbose than the reference 2-sentence target. The judge rubric penalizes coverage and conciseness.

4. **Translation occasionally adds material** — A subset of translations include details not in the English source, hurting the faithfulness component of the judge rubric.

---

## 6. Recommendations for the Mueen Team

Priority order (highest impact first):

**P1 — Improve Arabic NER coverage**
  - Collect more annotated Arabic news data with PERSON/LOCATION/ORGANIZATION tags including morphological variants and partial mentions.
  - Consider an explicit entity-extraction prompt scaffold during training/inference.

**P2 — Improve NLI claim handling**
  - Ensure the model strictly preserves provided claim text in classification tasks.
  - Investigate why NOT_ENOUGH_INFO (the hardest, weight 1.5) is missed most often.

**P3 — Tighten summary length**
  - Train/instruct the model to honor the 2-sentence target.
  - Penalize verbatim sentence copying explicitly.

**P4 — Reduce translation hallucinations**
  - Add faithfulness constraints to the translation prompt.
  - Consider a translation-specific fine-tuning pass on faithful Eng→Ar pairs.

**P5 — Reduce category variance**
  - Sports category (5.19) underperforms; investigate domain coverage in training data.

---

## 7. Reproducibility

All evaluation artifacts are captured in this repository:

- `arabic_500_dataset.json` — full corpus (500 articles)
- `selected_100.json` + `selected_next_100.json` — the 200-article evaluation set
- `mueen_results_full.json` — Mueen's outputs alongside reference data and scores
- `comparison_data.csv` — machine-readable scores for all 4 models × 200 articles
- `200-ARTICLE-EVALUATION.md` — high-level cross-model comparison
- `mueen_evaluation_samples.md` — 5 worked side-by-side examples
- `scripts/sample_100.py` — deterministic article sampler
- `scripts/run_benchmark.py` — end-to-end orchestration

---

*This report was generated from the live evaluation database by `scripts/build_mueen_report.py`. All numbers cross-verifiable against the underlying SQLite database and the JSON artifacts in this repository.*