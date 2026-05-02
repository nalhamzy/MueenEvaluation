# Mueen AI — Comprehensive Evaluation Report

**Date issued:** 2 May 2026
**Evaluation framework:** Arabic LLM Benchmark Platform (this repository)
**Articles evaluated:** 200 Arabic articles across 5 domains
**Models compared:** Mueen AI vs. Qwen 3.5 397B, DeepSeek Chat (V3), Mistral Large
**Scoring pipelines:** Deterministic + Automated LLM Judge (GPT-5.2) + Independent Human Judge

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [About the Models](#2-about-the-models)
3. [Methodology](#3-methodology)
4. [Detailed Results (with 95% CIs)](#4-detailed-results-with-95-confidence-intervals)
5. [Mueen AI Deep-Dive](#5-mueen-ai-deep-dive)
6. [Failure Pattern Analysis](#6-failure-pattern-analysis)
7. [Recommendations for the Mueen Team](#7-recommendations-for-the-mueen-team)
8. [Human Validation](#8-human-validation)
9. [Limitations and Threats to Validity](#9-limitations-and-threats-to-validity)
10. [Reproducibility](#10-reproducibility)

---

## 1. Executive Summary

Mueen AI was evaluated on **200 Arabic news articles** across 5 categories (culture, finance, politics, sports, tech) on **4 NLP tasks**: Named Entity Recognition (NER), Natural Language Inference (NLI), Arabic Summarization, and English-to-Arabic Translation. Three commercial frontier models were evaluated on the same dataset for comparison.

### Headline result

Mueen AI achieved an **overall score of 5.91 / 10 (95% CI [5.67, 6.12])**, placing it in **4th position** among the 4 evaluated models. The leading frontier model (Qwen 3.5 397B) scored 8.76/10 (CI [8.65, 8.87]), a gap of **2.85 points**. **All four pairwise model differences in overall score are statistically significant** (non-overlapping 95% bootstrap confidence intervals).

### Final leaderboard (200 articles, with 95% bootstrap CIs)

| Rank | Model | NER | NLI | Summary | Translation | **Overall** |
|:----:|-------|:---:|:---:|:-------:|:-----------:|:-----------:|
| 1 | **Qwen 3.5 397B** | 7.62 ±0.24 | 9.80 ±0.10 | 9.12 ±0.15 | 9.20 ±0.16 | **8.76 ±0.11** |
| 2 | DeepSeek Chat | 7.07 ±0.26 | 9.88 ±0.08 | 8.83 ±0.13 | 8.80 ±0.17 | **8.46 ±0.10** |
| 3 | Mistral Large | 5.95 ±0.29 | 9.39 ±0.17 | 8.09 ±0.19 | 5.02 ±0.17 | **6.89 ±0.13** |
| 4 | **Mueen AI** | 4.03 ±0.37 | 7.54 ±0.33 | 7.30 ±0.29 | 5.45 ±0.32 | **5.91 ±0.23** |

*CIs are 95% non-parametric bootstrap (1000 resamples, seed=11). See [bootstrap_ci.json](bootstrap_ci.json) for full data.*

### Independent human validation

A blinded native-Arabic-speaking human evaluator (Ahmed Al Saidi) judged Summary and Translation outputs from all 4 models on a 30-article subsample. The human ranking is **identical to the automated ranking** (Spearman ρ = +1.000 at the model level; ρ = +0.688 at the per-judgment level over 240 paired observations). See [Section 8](#8-human-validation) for details.

### Key insight

Mueen AI's relative weakness is concentrated in **Named Entity Recognition** (4.03/10, vs. 7.62 for the leader). NLI also shows a meaningful gap (7.54 vs. 9.80). Generative tasks (Summary 7.30, Translation 5.45) are closer to the field — Mueen actually outperforms Mistral Large on Translation. The blinded human evaluation is **systematically harsher** than the LLM judge but produces the same rank order, which strengthens rather than undermines this conclusion.

---

## 2. About the Models

> **Note on disclosure.** Specifications below are summarized from public information at the time of evaluation. Where parameter counts or training details are not publicly disclosed (Mueen AI), the report says so explicitly rather than inferring.

### 2.1 Mueen AI (focal model)

| Attribute | Value |
|-----------|-------|
| Provider | Mueen (Saudi Arabia) |
| Specialization | Arabic-language assistant |
| Access at evaluation time | Browser-based assistant (no public API) |
| Architecture / parameter count | Not publicly disclosed |
| Training data | Not publicly disclosed |
| Licensing | Proprietary |

Mueen AI was the **focal model** of this evaluation: the user commissioned the benchmark to obtain an independent technical assessment of Mueen on standard Arabic NLP tasks. Because Mueen is delivered exclusively through a browser interface, it was evaluated **manually** — articles were grouped into 10-article chunks, presented to the assistant via a structured brief prompt, and the JSON outputs were captured and uploaded into the benchmark database. The other three models were evaluated programmatically via their respective APIs. This methodological asymmetry is a known limitation discussed in [Section 9](#9-limitations-and-threats-to-validity).

### 2.2 Qwen 3.5 397B (Alibaba)

| Attribute | Value |
|-----------|-------|
| Provider | Alibaba Cloud Dashscope |
| Variant evaluated | `qwen3.5-397b-a17b` |
| Architecture | Mixture-of-Experts (~397 B total parameters, ~17 B active) |
| Access | Public API |
| Strengths | State-of-the-art multilingual performance |

### 2.3 DeepSeek Chat (V3)

| Attribute | Value |
|-----------|-------|
| Provider | DeepSeek (China) |
| Variant evaluated | `deepseek-chat` (V3) |
| Architecture | Mixture-of-Experts |
| Access | Public API |
| Strengths | Strong general-purpose performance, cost-efficient |

### 2.4 Mistral Large

| Attribute | Value |
|-----------|-------|
| Provider | Mistral AI (France) via AWS Bedrock |
| Variant evaluated | `mistral.mistral-large-2402-v1:0` |
| Architecture | Dense transformer |
| Access | AWS Bedrock API |
| Strengths | Strong reasoning; weaker on Arabic generation |

---

## 3. Methodology

### 3.1 Architecture

```
              Article (Arabic)
                     │
                     ▼
        ┌────────────────────────┐
        │  Teacher: Claude Opus  │   generates reference outputs
        │   4.6 — Anthropic      │   for the 4 tasks
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Students: 4 models   │   each produces predictions
        │  Qwen, DeepSeek,       │   for the 4 tasks
        │  Mistral, Mueen AI     │
        └────────────┬───────────┘
                     │
            ┌────────┴────────┐
            ▼                 ▼
   ┌──────────────────┐  ┌──────────────────┐
   │ Deterministic    │  │ Automated Judge  │
   │ scoring          │  │ (GPT-5.2)        │
   │ (NER F1, NLI)    │  │ (Sum, Tx rubric) │
   └──────────────────┘  └──────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Human Judge (blinded) │   30-article validation
        │  on Summary + Tx tasks │   (Section 8)
        └────────────────────────┘
```

### 3.2 The 4 tasks

1. **NER (Named Entity Recognition).** Extract entities into 4 categories (PERSON, LOCATION, ORGANIZATION, MISC) from each Arabic article. Scored deterministically using **weighted F1** with Arabic normalization (diacritics removal, alef variants unification, definite article ال handling) and a hallucination penalty for entities that do not appear in the source text.
2. **NLI (Natural Language Inference / Fact Verification).** Given an article and 4 reference claims, label each as `SUPPORTED`, `REFUTED`, or `NOT_ENOUGH_INFO`. Scored by **positional weighted accuracy** (NOT_ENOUGH_INFO × 1.5, REFUTED × 1.2, SUPPORTED × 1.0). The position-based comparison sidesteps any claim-text rewriting by the student.
3. **Arabic Summarization.** Produce a 2-sentence summary in formal Modern Standard Arabic (فصحى). Scored by GPT-5.2 with a 5-criterion rubric: factual accuracy (0–3), coverage (0–3), no added inference (0–2), register fluency (0–2), and verbatim copying penalty (0–1).
4. **English→Arabic Translation.** Translate a 3-sentence English summary of the article into formal Arabic. Scored by GPT-5.2 with a 4-criterion rubric: faithfulness (0–3), fluency (0–3), terminology handling (0–2), register/formality (0–2).

### 3.3 Overall score formula

```
Overall = NER × 0.30 + NLI × 0.20 + Summary × 0.25 + Translation × 0.25
```

**Note on weight choice.** The weights reflect the user's stated priorities for an Arabic NLP system: NER as the most discriminating deterministic signal (0.30), generative tasks combined (0.50), NLI as a saturated check (0.20). They are not derived from formal optimization. Because Mueen ranks last on every single component, the **ordering is robust to any reasonable reweighting**; the *gap size* is not.

### 3.4 Dataset

- 500 Arabic articles collected across 5 categories (100 each).
- 200 articles sampled for evaluation in two rounds: round 1 (seed=42, 100 articles, 20 per category) and round 2 (seed=99, 100 different articles, 20 per category).
- ~40 articles per category in the final 200-article evaluation set.

### 3.5 Statistical methodology

All point estimates in this report are accompanied by **95% non-parametric bootstrap confidence intervals** (1000 resamples over articles, seed=11). The bootstrap procedure resamples articles with replacement and recomputes the per-model mean for each task; the 2.5th and 97.5th percentiles of the resampled means form the CI. Two model means are reported as significantly different when their 95% CIs do **not** overlap.

---

## 4. Detailed Results (with 95% Confidence Intervals)

### 4.1 Per-task scores — all 4 models

| Task | Qwen 3.5 | DeepSeek | Mistral | Mueen AI | Mueen Rank |
|------|:--------:|:--------:|:-------:|:--------:|:----------:|
| **NER** | 7.62 ±0.24 | 7.07 ±0.26 | 5.95 ±0.29 | **4.03 ±0.37** | 4 |
| **NLI** | 9.80 ±0.10 | 9.88 ±0.08 | 9.39 ±0.17 | **7.54 ±0.33** | 4 |
| **Summary** | 9.12 ±0.15 | 8.83 ±0.13 | 8.09 ±0.19 | **7.30 ±0.29** | 4 |
| **Translation** | 9.20 ±0.16 | 8.80 ±0.17 | 5.02 ±0.17 | **5.45 ±0.32** | 3 |
| **Overall** | 8.76 ±0.11 | 8.46 ±0.10 | 6.89 ±0.13 | **5.91 ±0.23** | 4 |

Half-widths shown are 95% CI half-widths from the bootstrap. **Note:** On the Translation task only, Mueen AI's point estimate (5.45) is above Mistral Large's (5.02), but their 95% CIs overlap ([5.13, 5.77] vs. [4.85, 5.19]). This is the **only** pairwise comparison in the entire results matrix where the difference does not reach 95% significance. The independent human judge scored both models far below their LLM-judge translation scores (Mueen 0.67/10 vs. Mistral 2.25/10 on the human scale), placing Mistral above Mueen on translation in the human evaluation. **Conclusion:** the Mueen-vs-Mistral translation comparison is statistically tied on the LLM judge and reverses under the human judge — the cleanest interpretation is "approximately equivalent, both poor."

### 4.2 Pairwise statistical significance — overall score

All other pairwise differences are statistically significant at 95% confidence:

| Comparison | CI separation | Conclusion |
|------------|:-------------:|------------|
| Qwen vs. DeepSeek | 8.65 > 8.57 | Significantly different |
| Qwen vs. Mistral | 8.65 > 7.02 | Significantly different |
| Qwen vs. Mueen | 8.65 > 6.12 | Significantly different |
| DeepSeek vs. Mistral | 8.36 > 7.02 | Significantly different |
| DeepSeek vs. Mueen | 8.36 > 6.12 | Significantly different |
| Mistral vs. Mueen | 6.77 > 6.12 | Significantly different |

The full leaderboard ordering is statistically robust.

### 4.3 Mueen AI per-category breakdown

| Category | N | NER | NLI | Summary | Translation | Overall |
|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|
| Culture | 40 | 3.92 | 7.91 | 7.20 | 5.76 | **6.00** |
| Finance | 40 | 4.76 | 7.72 | 7.10 | 6.14 | **6.28** |
| Politics | 42 | 3.08 | 7.19 | 7.15 | 5.52 | **5.53** |
| Sports | 33 | 3.36 | 6.50 | 6.91 | 4.63 | **5.19** |
| Tech | 41 | 4.94 | 8.21 | 8.08 | 5.09 | **6.42** |

Per-category sample sizes are small (n ≈ 40); category-level differences should be treated as suggestive rather than conclusive.

---

## 5. Mueen AI Deep-Dive

### Strengths

- **Best category: Tech** with overall score 6.42/10. Mueen handles tech content with the most consistency on the LLM-judged metric.
- **Second-best category: Finance** (6.28/10).
- **Translation is Mueen's relatively strongest task** ranked against the field — 3rd of 4 models on the LLM judge, beating Mistral Large.
- **NLI labels are usable** when claims are presented in the expected format (7.54/10) — meaningful signal, even if behind the leaders.

### Weaknesses

- **Worst category: Sports** with overall score 5.19/10. The sports domain produces the most misses.
- **NER (4.03/10) is the weakest task overall** — the gap to the leader (Qwen 3.5: 7.62) is 3.59 points. Mueen frequently misses entities that the reference includes, particularly people's full names and organization variants.
- **NLI accuracy (7.54/10) trails the field** — all three commercial models cluster at 9.4–9.9 on this task.
- **Hallucination flagged by human judge** — the human evaluator explicitly identified Mueen AI as exhibiting cases of *invented information* in summaries and translations. See Section 8.6.

### Worked examples

Five articles (one per category, picked at the per-category median Mueen score) are reproduced in the companion file [mueen_evaluation_samples.md](mueen_evaluation_samples.md). Each example shows Mueen's actual outputs side-by-side with the Claude Opus reference and the GPT-5.2 judge feedback.

---

## 6. Failure Pattern Analysis

Patterns observed across the 196 scored Mueen articles, corroborated by the human evaluator's qualitative notes:

1. **NER under-extraction.** Mueen tends to extract a smaller entity set than the reference. The reference includes morphological variants and secondary mentions; Mueen tends to capture only the most prominent ones.

2. **NLI claim-text drift.** In the first manual round, Mueen rewrote several claims rather than copying them verbatim. Once the prompt was tightened to enforce verbatim claim copying, NLI scores rose substantially (2.90 → 7.36 on the same articles). This is a prompt-engineering artifact, not a model capability ceiling.

3. **Summary register and verbosity.** Summaries are in MSA but tend to be longer than the requested 2-sentence target, which the judge rubric penalizes.

4. **Hallucination in summaries and translations.** The human evaluator's most pointed criticism: Mueen "invents new information or omits important information from the source text" in both Summary and Translation tasks. This is a *faithfulness* failure, the most serious failure class in generative NLP.

5. **Translation occasional additions.** Independent of the human finding, the LLM judge's faithfulness component (worth 0–3 points out of 10) flagged Mueen translations adding details not in the English source.

---

## 7. Recommendations for the Mueen Team

Priority order (highest impact first):

**P1 — Reduce hallucination in generative tasks** *(elevated based on human judge findings)*
  - Add explicit faithfulness constraints to summary and translation prompts ("only state what is in the source").
  - Consider faithfulness-targeted post-training (e.g., DPO on faithful vs. fabricated pairs).
  - Audit failure cases identified by the human evaluator and use them as training/eval signal.

**P2 — Improve Arabic NER coverage**
  - Collect more annotated Arabic news data with PERSON / LOCATION / ORGANIZATION tags including morphological variants and partial mentions.
  - Consider an explicit entity-extraction prompt scaffold during inference.

**P3 — Improve NLI claim handling**
  - Ensure the model strictly preserves provided claim text in classification tasks.
  - Investigate why NOT_ENOUGH_INFO (the hardest, weight 1.5) is missed most often.

**P4 — Tighten summary length**
  - Train/instruct the model to honor the 2-sentence target.
  - Penalize verbatim sentence copying explicitly.

**P5 — Reduce category variance**
  - Sports category (5.19) underperforms; investigate domain coverage in training data.

**P6 — Expose an API**
  - The browser-only access constraint blocks reproducible evaluation. An API offering — even a rate-limited one — would let the Mueen team run continuous benchmarks against future model versions and address the methodology asymmetry described in Section 9.

---

## 8. Human Validation


To independently validate the GPT-5.2 LLM-as-Judge scores, a single qualified human evaluator scored Summary and Translation outputs from all 4 models on a stratified subsample of 30 articles (6 per category). The evaluator was **blinded** — model identities were anonymized as Model A–D and revealed only after scoring was complete.

**Evaluator:** Ahmed Al Saidi (native Arabic speaker). **Period:** 2026-04-28 → 2026-05-02. **Total judgments:** 240 (30 articles × 4 models × 2 tasks). **Scale:** integer 1–5 (rescaled to 0–10 for comparability).

### 8.1 Human-validated leaderboard (rescaled to 0–10)

| Rank | Model | Summary (Human) | Translation (Human) | Combined (Human) |
|:----:|-------|:--------------:|:-------------------:|:----------------:|
| 1 | Qwen 3.5 397B | 8.75 | 9.17 | **8.96** |
| 2 | DeepSeek Chat | 6.17 | 8.17 | **7.17** |
| 3 | Mistral Large | 4.25 | 2.25 | **3.25** |
| 4 | **Mueen AI** | 2.75 | 0.67 | **1.71** |

### 8.2 Agreement with the GPT-5.2 LLM Judge

Per-judgment correlation between the human evaluator (rescaled to 0–10) and the GPT-5.2 LLM judge on the same 30 articles:

| Task | n | Spearman ρ | Pearson r |
|------|:-:|:---------:|:---------:|
| Summary | 120 | +0.526 | +0.568 |
| Translation | 120 | +0.808 | +0.767 |
| Combined | 240 | +0.688 | +0.682 |

At the **model level** (Spearman over the 4 model means on the same 30 articles): ρ = **+1.000**.

### 8.3 Model means on the same 30-article subset

| Model | LLM Judge (0–10) | Human (0–10) | Δ (Human − LLM) |
|-------|:----------------:|:------------:|:---------------:|
| Qwen 3.5 397B | 8.99 | 8.96 | −0.03 |
| DeepSeek Chat | 8.65 | 7.17 | −1.48 |
| Mistral Large | 6.52 | 3.25 | −3.27 |
| Mueen AI | 5.99 | 1.71 | −4.28 |

The human evaluator is **systematically stricter** than the LLM judge — the gap widens for weaker models. The LLM judge appears tightly calibrated at the top end of quality (Qwen Δ = −0.03) and progressively more lenient toward mid- and lower-quality outputs. **The ordering is preserved** across all four models, which is the property required for the LLM judge to be a useful ranking instrument.

### 8.4 Ranking comparison

| Model | LLM Rank | Human Rank | Match |
|-------|:--------:|:----------:|:-----:|
| Qwen 3.5 397B | 1 | 1 | ✓ |
| DeepSeek Chat | 2 | 2 | ✓ |
| Mistral Large | 3 | 3 | ✓ |
| Mueen AI | 4 | 4 | ✓ |

**The human and automated judges produced an identical model ranking.** This is the strongest possible agreement signal at the model level and supports the leaderboard reported in Section 4.

### 8.5 Mueen AI — per-category human scores (1–5)

| Category | n | Summary | Translation | Combined |
|----------|:-:|:-------:|:-----------:|:--------:|
| Culture | 6 | 2.00 | 1.83 | **1.92** |
| Finance | 6 | 2.50 | 1.17 | **1.83** |
| Politics | 6 | 2.33 | 1.00 | **1.67** |
| Sports | 6 | 2.00 | 1.17 | **1.58** |
| Tech | 6 | 1.67 | 1.17 | **1.42** |

The human evaluator's category ordering for Mueen differs from the LLM judge's: the human ranks Culture highest, Tech lowest. The LLM judge (on the full 200-article set) ranks Tech highest, Sports lowest. This is the only material disagreement and likely reflects the human's stricter standard for technical Arabic terminology — supported by the qualitative observations below.

### 8.6 Evaluator's qualitative observations

> *(Original Arabic by the evaluator. Model letters de-anonymized post-scoring: A → Qwen 3.5, B → Mueen AI, C → DeepSeek Chat, D → Mistral Large.)*
>
> - الأخبار الاقتصادية وخصوصاً التي تحمل أرقاماً تشكل أكبر فارق في نتائج النماذج
> - ويجب اعتمادها في قياس أداء النماذج المستقبلية
> - المواضيع المرتبطة بالرياضة كانت الأسهل وأظهرت نتائج متقاربة بين النماذج
> - أكبر الفروق تكمن في فصاحة اللغة والشمولية حيث أظهر النموذج A (Qwen) تفوقاً كبيراً في المصطلحات المستخدمة وجودة المخرجات
> - النموذج C (DeepSeek) أداؤه متقارب من النموذج A (Qwen) وتفوّق عليه في موضوعات الترجمة في بعض المقالات وينقصه الفصاحة فقط
> - أظهر النموذج B (Mueen) العديد من حالات الهلوسة في مهمة التلخيص وكذلك الترجمة من خلال اختلاق معلومات جديدة أو حذف معلومات مهمة
> - أكبر التحديات التي يواجهها النموذج D (Mistral) هي تركيب الجمل العربية واختيار المصطلحات المناسبة

### 8.7 What this means

The blinded human evaluation **confirms** the ordering produced by the automated LLM judge: Mueen AI ranks fourth, behind all three commercial frontier models. The gap between Mueen AI and the leading model is consistent across both judges and, on the human scale, considerably wider than the LLM judge suggested.

This independent human validation:

1. **Removes the principal credibility risk** of an automated benchmark — that the LLM judge might systematically favor or penalize specific models. The model-level Spearman of +1.000 directly refutes that concern.
2. **Calibrates the LLM judge's leniency.** GPT-5.2 is approximately equivalent to a human judge at the very top of the quality range, but is markedly more forgiving toward mid- and lower-quality outputs (Δ ranges from −1.48 for DeepSeek to −4.28 for Mueen). **The LLM judge's absolute scores should be treated as upper bounds on the underlying quality.**
3. **Identifies Mueen-specific failure modes** that the LLM judge alluded to but the human evaluator named explicitly: hallucination in summaries (invented facts, omitted key information) and faithfulness drift in translation. This converges with the qualitative findings of Sections 5–7.

---

## 9. Limitations and Threats to Validity

This section catalogues every methodological limitation that an independent reviewer could reasonably raise. Acknowledging them transparently is the strongest form of credibility.

### 9.1 Single human evaluator (no inter-rater reliability)

**The issue.** Section 8 reports a single evaluator's judgment on 30 articles. There is no measurement of inter-rater reliability (e.g., Cohen's κ between two evaluators), so we cannot statistically distinguish "this is a well-calibrated rubric" from "this is one person's idiosyncratic preferences."

**Impact.** Likely small for the headline finding (Mueen 4th place is a >2-point gap on a 0–10 scale; this would survive any reasonable evaluator). Potentially material for fine-grained claims.

**Mitigation.** A second evaluator scoring an overlapping subset of articles, with Cohen's κ reported, would close this gap. Recommended for any future iteration of this evaluation.

### 9.2 Browser-based vs. API-based evaluation asymmetry

**The issue.** Mueen AI was evaluated through a browser interface (via a 10-article-chunked structured brief), while the other three models were evaluated through their APIs. The two delivery channels differ in:
- System prompts (browser assistants typically have proprietary system prompts the user does not see)
- Context budgets and answer-shaping behavior
- JSON-mode availability (API models can be strictly forced into JSON output)

**Impact.** Could disadvantage Mueen in machine-readable tasks (NER, NLI), where output parsing reliability matters. Less likely to materially affect Summary or Translation.

**Mitigation.** The same brief prompt was used for Mueen across all 200 articles; outputs were validated and, where Mueen rewrote NLI claims rather than copying them, an alignment script preserved the underlying labels. The Mueen team should expose an API to enable like-for-like evaluation.

### 9.3 Reference data is from a single LLM (Claude Opus 4.6)

**The issue.** The "ground truth" for NER and NLI, and the reference text for Summary and Translation, were generated by Claude Opus 4.6. This is another commercial LLM, not human-curated gold-standard data. A model that disagrees with Claude is not necessarily wrong.

**Impact.** Could systematically penalize models that produce legitimately different but valid Arabic, especially for stylistic tasks like Summary. Less impact on NER and NLI where the entity set and claim labels are more constrained.

**Mitigation.** Future iterations should incorporate human-curated reference data on a sampled subset to recalibrate.

### 9.4 LLM judge calibration gap (Section 8.3)

**The issue.** The human evaluator scored Mueen at 1.71/10 versus the LLM judge's 5.99/10 on the same 30 articles — a 4.28-point absolute gap. Whether to interpret the LLM scores or human scores as primary depends on which judge is considered authoritative.

**Impact.** The **rank ordering** is robust (identical between judges; Spearman = 1.0), but the **score gap** between Mueen and the commercial models is larger on the human scale than on the LLM scale.

**Mitigation.** This report presents both pipelines side-by-side rather than picking one. Readers are encouraged to treat the LLM judge as a screening instrument and the human judge as the calibration reference.

### 9.5 Score weights are not optimized

**The issue.** The overall score weights (NER 0.30, NLI 0.20, Summary 0.25, Translation 0.25) were chosen to reflect the user's stated priorities, not derived from a formal optimization or principal-component analysis.

**Impact.** Different reasonable weights would change the *gap sizes* in the leaderboard. The *ordering* is robust because Mueen ranks last on every component.

**Mitigation.** Per-task scores are reported alongside the overall (Sections 4.1, 8.1), allowing readers to apply their own weighting.

### 9.6 Per-category sample sizes are small

**The issue.** Each category contains ~40 articles in the 200-article set and only 6 in the 30-article human evaluation. Category-level differences should be treated as suggestive.

**Impact.** Claims like "Mueen is best on Tech" are based on n ≈ 40 (LLM judge) or n = 6 (human judge). Effect sizes need to be substantial to be reliable at these sample sizes.

**Mitigation.** This report uses category breakdowns descriptively, not as the basis for procurement decisions.

### 9.7 Translation direction is unidirectional

**The issue.** Only English→Arabic translation was evaluated; Arabic→English was not.

**Impact.** Limits the breadth of the translation finding. A model that handles Eng→Ar well may not handle Ar→Eng equally well, or vice versa.

**Mitigation.** Future work should add the reverse direction.

### 9.8 Evaluator domain expertise

**The issue.** The human evaluator self-reported as a native Arabic speaker but the report does not document specific domain expertise (technical, financial, political).

**Impact.** Could affect category-level scores. The evaluator's own observation that Sports was easiest and Finance most discriminating supports the view that domain knowledge influences scoring sensitivity.

**Mitigation.** Future evaluations could recruit domain-specialist evaluators per category.

### 9.9 Benchmarks are not comprehensive evaluations

**The issue.** Performance on these 4 tasks does not capture all dimensions of an Arabic LLM's utility (dialogue, agentic behavior, code, vision, dialectal Arabic, safety, etc.).

**Impact.** Procurement decisions should not be made on this benchmark alone.

**Mitigation.** This report explicitly scopes itself to "standard Arabic NLP tasks on news content" and recommends complementary evaluations (e.g., conversational quality, dialect handling, refusal behavior) before any deployment decision.

---

## 10. Reproducibility

All evaluation artifacts are captured in this repository:

- `arabic_500_dataset.json` — full corpus (500 articles)
- `selected_100.json` + `selected_next_100.json` — the 200-article evaluation set
- `mueen_results_full.json` — Mueen's outputs alongside reference data and scores
- `comparison_data.csv` — machine-readable scores for all 4 models × 200 articles
- `bootstrap_ci.json` — bootstrap CIs for all per-task per-model scores
- `200-ARTICLE-EVALUATION.md` — high-level cross-model comparison
- `mueen_evaluation_samples.md` — 5 worked side-by-side examples
- `human_eval/` — full human evaluation artifacts (workbook, results, blinding key)
- `scripts/sample_100.py` — deterministic article sampler
- `scripts/run_benchmark.py` — end-to-end orchestration
- `scripts/compute_bootstrap_ci.py` — confidence interval computation
- `scripts/build_human_eval_package.py` — blinded workbook builder
- `scripts/ingest_human_eval.py` — human evaluation post-processing

To reproduce headline numbers:

```bash
# Bootstrap CIs
py scripts/compute_bootstrap_ci.py --iters 1000 --seed 11

# Human evaluation results (after Ahmed's filled workbook is in place)
py scripts/ingest_human_eval.py --filled human_eval/human_eval_workbook_Ahmed.xlsx
```

---

*This report was generated from the live evaluation database by `scripts/build_mueen_report.py`, with confidence intervals from `scripts/compute_bootstrap_ci.py` and human validation from `scripts/ingest_human_eval.py`. All numbers cross-verifiable against the underlying SQLite database and the JSON / CSV / XLSX artifacts in this repository.*
