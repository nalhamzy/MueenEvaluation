# Limitations and Threats to Validity — Mueen AI Evaluation

**Companion document to:** `MUEEN_EVALUATION_REPORT_EN.md`, `MUEEN_EVALUATION_LETTER_AR.md`
**Date:** 2 May 2026

This document catalogues every methodological limitation that an independent reviewer could reasonably raise about the Mueen AI evaluation. It is provided as a standalone artifact so that any party reviewing the evaluation has a single, authoritative reference for the study's known weaknesses.

> **Principle:** Acknowledged limitations strengthen credibility; hidden limitations destroy it when discovered.

---

## Summary table

| # | Limitation | Severity | Affects | Mitigation |
|:-:|------------|:--------:|---------|------------|
| 1 | Single human evaluator (no IRR) | Medium | Section 8 | Add a 2nd evaluator, report Cohen's κ |
| 2 | Browser vs. API asymmetry for Mueen | Medium-High | All Mueen scores | Mueen team to expose API |
| 3 | Reference data from a single LLM | Medium | All scores | Sampled human-curated gold |
| 4 | LLM judge calibration gap | Low (rank) / High (absolute) | Sections 3-4 | Reported alongside human scores |
| 5 | Score weights not optimized | Low | Overall ranking | Per-task scores reported |
| 6 | Small per-category samples | Low | Category claims | Treat as descriptive only |
| 7 | Translation direction unidirectional | Low | Translation finding | Add Ar→Eng in future |
| 8 | Evaluator domain expertise | Low | Category scores | Recruit domain specialists |
| 9 | Benchmarks ≠ comprehensive eval | Low (scope) | Procurement | Run complementary tests |

---

## 1. Single human evaluator (no inter-rater reliability)

### The issue
The human validation in [Section 8 of the report](MUEEN_EVALUATION_REPORT_EN.md#8-human-validation) reports a single evaluator's judgment on 30 articles (240 individual judgments). There is no measurement of inter-rater reliability — i.e., we cannot statistically distinguish "this is a well-calibrated rubric applied consistently" from "this is one person's idiosyncratic preferences."

### Why it matters
Single-evaluator results are the standard floor of credibility for human-evaluation work in NLP. They are publishable and defensible but cannot speak to the *generalizability* of the rubric. Two evaluators scoring an overlapping subset would yield a Cohen's κ statistic measuring how reproducible the rubric is across humans.

### Impact on this evaluation
**Likely small** for the headline finding. Mueen ranks 4th by a >2-point gap on a 0–10 scale. This margin would survive virtually any reasonable evaluator's idiosyncrasies. The model-level Spearman of +1.000 between human and LLM judge is itself an external check, providing partial reassurance.

**Potentially material** for fine-grained claims, especially:
- The relative ranking of Mistral Large vs. Mueen on Translation, where the LLM and human judges disagree.
- Per-category orderings within Mueen's results.

### Recommended mitigation
For any future iteration, recruit a second evaluator (different background, same blinding process) to score an overlapping ~15-article subset. Report Cohen's κ alongside the existing scores.

---

## 2. Browser-based vs. API-based evaluation asymmetry

### The issue
Mueen AI was evaluated through its **browser interface** (because no public API exists at the time of this evaluation). Articles were grouped into 10-article chunks, presented via a structured "brief" prompt, and the JSON outputs were captured manually and uploaded to the database. The other three models (Qwen, DeepSeek, Mistral) were evaluated **programmatically** via their respective APIs.

The two delivery channels differ in:
- **System prompts:** Browser assistants typically have proprietary system prompts that the user does not control or see.
- **Context budgets and output shaping:** Browser interfaces may have answer-length limits, formatting preferences, or hidden truncation that don't apply to API calls.
- **JSON-mode availability:** API models can be forced into strict JSON output (using `response_format`); browser-based assistants must be coaxed via prompt engineering.
- **Inter-task isolation:** Browser sessions accumulate context; API calls are typically stateless.

### Why it matters
This is the single most legitimate fairness complaint a Mueen partisan could raise. If Mueen's true model is competitive but its delivery channel is impaired, the published scores understate its capability.

### Impact on this evaluation
- **Most likely affected:** NER and NLI scores (machine-readable tasks where output parsing reliability matters most). The first NLI run had to be re-aligned because Mueen rewrote claims rather than copying them verbatim — likely a browser-prompting artifact.
- **Less likely affected:** Summary and Translation, which are evaluated as natural-language text by GPT-5.2 and a human, and are robust to formatting variations.

The ranking is unlikely to flip — Mueen is 4th on every individual component and on the human evaluation, which is conducted on the model outputs as text and is therefore symmetric across delivery channels. But the absolute Mueen scores could realistically be 0.5–1.0 points higher under API-based evaluation.

### Recommended mitigation
The Mueen team should expose an API (rate-limited is sufficient) and re-run the benchmark. This would also enable continuous evaluation as Mueen iterates.

---

## 3. Reference data is generated by a single LLM (Claude Opus 4.6)

### The issue
The "ground truth" for NER and NLI tasks, and the reference text for Summary and Translation tasks, were generated by **Claude Opus 4.6**. This is another commercial LLM, not human-curated gold-standard data. A model that disagrees with Claude Opus is not necessarily wrong.

### Why it matters
This is the standard limitation of LLM-as-teacher methodologies. The reference set inherits whatever blind spots, biases, or stylistic preferences the teacher model has. Claude Opus is widely regarded as a strong Arabic model, but it is not native human linguistic intuition.

### Impact on this evaluation
- **Constrained for NER:** Entity sets are mostly objective (a name is a name); little teacher subjectivity.
- **Constrained for NLI:** Claim labels (SUPPORTED/REFUTED/NOT_ENOUGH_INFO) are mostly objective for well-written claims.
- **Larger for Summary:** Two valid summaries can differ stylistically; the rubric scores against the reference, so a model with a different but valid Arabic style is penalized.
- **Larger for Translation:** Multiple valid translations exist; the LLM judge has access to the reference and may anchor on it.

### Recommended mitigation
Future iterations should incorporate **human-curated reference data on a sampled subset** to recalibrate the teacher's outputs against native-speaker judgment.

---

## 4. LLM judge absolute calibration gap

### The issue
The blinded human evaluator scored Mueen at **1.71/10** versus the LLM judge's **5.99/10** on the same 30 articles — a 4.28-point absolute gap. The deltas are non-uniform across models (see table below).

| Model | LLM Judge (0–10) | Human (0–10) | Δ |
|-------|:--:|:--:|:--:|
| Qwen 3.5 397B | 8.99 | 8.96 | −0.03 |
| DeepSeek Chat | 8.65 | 7.17 | −1.48 |
| Mistral Large | 6.52 | 3.25 | −3.27 |
| Mueen AI | 5.99 | 1.71 | −4.28 |

### Why it matters
Two interpretations are possible:
1. **Charitable:** GPT-5.2 is well-calibrated at the top of the quality range and progressively more lenient toward weaker outputs. The ordering is preserved (Spearman = +1.000), so the ranking is reliable.
2. **Skeptical:** GPT-5.2 is unreliable on Arabic generation when quality drops, and the headline 5.91/10 score for Mueen is meaningfully inflated.

### Impact on this evaluation
The **rank ordering** is robust and not in dispute. The **score gap** between models is larger on the human scale than on the LLM scale.

### Recommended mitigation
This report explicitly presents both pipelines side-by-side. Readers should treat **the LLM judge as a screening instrument and the human judge as the calibration reference**. The report's framing has been updated (Section 8.7) to reflect this.

---

## 5. Score weights are not formally optimized

### The issue
The overall score is a weighted average:

```
Overall = NER × 0.30 + NLI × 0.20 + Summary × 0.25 + Translation × 0.25
```

These weights reflect the user's stated priorities: NER as the most discriminating deterministic signal (0.30), generative tasks combined (0.50), NLI as a saturated check (0.20). They were not derived from a principal-component analysis or an optimization against any external criterion.

### Impact
**Different reasonable weights would change the *gap sizes* in the leaderboard.** They would *not* change the ordering: Mueen ranks last on every individual component. The report consistently presents per-task scores alongside the overall, allowing readers to apply their own weighting.

### Mitigation
None required for ordering claims. For score-gap claims, recompute under alternative weights and verify robustness.

---

## 6. Small per-category sample sizes

### The issue
- 200-article evaluation: ~40 articles per category × 5 categories.
- 30-article human evaluation: 6 articles per category.

### Impact
Per-category claims are based on small samples. Effect sizes need to be substantial to be statistically reliable. Bootstrap CIs at the per-category level (not reported in the main tables for brevity) would be wider than the overall CIs.

### Mitigation
Treat per-category breakdowns as **descriptive**, not as the basis for procurement or training-data decisions.

---

## 7. Translation direction is unidirectional

### The issue
Only **English → Arabic** translation was evaluated. The reverse direction (Arabic → English) was not tested.

### Impact
A model can be strong in one direction and weaker in the other, especially for low-resource languages. The Translation finding generalizes only to Eng→Ar.

### Mitigation
Add Ar→Eng to a future iteration of the benchmark.

---

## 8. Evaluator domain expertise is undocumented

### The issue
The human evaluator (Ahmed Al Saidi) self-reported as a **native Arabic speaker** and rated his own confidence in the scoring, but the report does not document specific subject-matter expertise (technical, financial, political, sports).

### Impact
The evaluator's own qualitative observation that Sports was the easiest domain and Finance the most discriminating is consistent with the view that **domain knowledge influences scoring sensitivity**. Per-category Mueen scores under the human evaluator may reflect the evaluator's variable familiarity with each domain as well as the model's actual performance.

### Mitigation
For future iterations, recruit domain specialists per category, or use the same generalist evaluator with disclosed background information.

---

## 9. Benchmarks are not comprehensive evaluations

### The issue
Performance on these 4 NLP tasks (NER, NLI, Summary, Translation) does not capture all dimensions of an Arabic LLM's utility. **Out of scope:**

- Conversational dialogue quality
- Agentic / tool-use behavior
- Code generation
- Multimodal capabilities (vision, audio)
- Dialectal Arabic handling
- Safety, refusal behavior, jailbreak resistance
- Latency, throughput, cost

### Impact
**Procurement or deployment decisions should not be made on this benchmark alone.** A model that performs well on news-content NER might be unfit for a customer-facing chatbot, and vice versa.

### Mitigation
Use this report as **one input** in a broader evaluation portfolio. Recommended complements:
- Conversational evaluation on real user queries
- Dialect-specific test sets
- Safety / red-teaming evaluation
- Operational-cost benchmarks

---

## What this evaluation *does* support

Despite the limitations above, the following claims are **well-supported** by the data:

1. **Mueen AI ranks 4th of 4 evaluated models on standard Arabic NLP tasks for news content.** Statistically significant on every component (Section 4.2 of the report) and reproduced under blinded human evaluation.
2. **The gap between Mueen AI and the leading commercial models is substantial** (≥2.85 points on a 0–10 scale on the LLM judge; ≥7.25 points on the human scale).
3. **Mueen AI's primary weaknesses are NER coverage and hallucination in generative tasks**, the latter explicitly named by the human evaluator.
4. **The LLM-as-judge methodology is internally consistent** — its model-level rankings are validated by independent human evaluation (Spearman = +1.000).

These conclusions are robust to the limitations enumerated above.

---

## Document version

- **v1** — 2026-04-16: initial release with automated benchmark only.
- **v2** — 2026-05-02: added human validation (Section 8 of report); this Limitations document created as standalone artifact.
