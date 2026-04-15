"""Build the Mueen AI evaluation deliverable package.

Generates 6 files in the project root:
  1. mueen_results_full.json       — combined Mueen outputs + scores + reference
  2. comparison_data.csv           — machine-readable scores for all 4 models
  3. MUEEN_EVALUATION_REPORT_EN.md — full English technical report
  4. mueen_evaluation_samples.md   — 5 worked side-by-side examples
  5. خطاب_تقييم_معين.md            — Arabic official letter (cover)
  6. ATTACHMENTS_LIST.md           — list of attachments to deliver

Run from project root:
    py scripts/build_mueen_report.py
"""

import csv
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from statistics import median

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from database import SessionLocal
from models import (
    Article, DatasetItem, EvaluationRun, ModelOutput,
    RunStatus, OutputStatus,
)


CATEGORIES = ["culture", "finance", "politics", "sports", "tech"]
MODELS_OF_INTEREST = [
    "qwen3.5-397b-a17b",
    "deepseek-chat",
    "mistral.mistral-large-2402-v1:0",
    "Mueen AI",
]
MODEL_DISPLAY = {
    "qwen3.5-397b-a17b": "Qwen 3.5 397B-A17B",
    "deepseek-chat": "DeepSeek Chat (V3)",
    "mistral.mistral-large-2402-v1:0": "Mistral Large",
    "Mueen AI": "Mueen AI",
}


# ============================================================
# Step 1: Gather data
# ============================================================

def gather_data():
    """Build a unified view of all model outputs + reference data."""
    db = SessionLocal()
    try:
        runs = db.query(EvaluationRun).filter(
            EvaluationRun.status == RunStatus.COMPLETED
        ).all()

        # model_name -> {article_id -> ModelOutput} (latest wins on dup)
        model_outputs = defaultdict(dict)
        for r in runs:
            outs = db.query(ModelOutput).filter(
                ModelOutput.run_id == r.id,
                ModelOutput.status == OutputStatus.SCORED,
            ).all()
            for o in outs:
                if o.article_id.startswith("ART_"):
                    continue  # skip very early test runs
                prev = model_outputs[r.model_name].get(o.article_id)
                if prev is None or (
                    o.processed_at and prev.processed_at
                    and o.processed_at > prev.processed_at
                ):
                    model_outputs[r.model_name][o.article_id] = o

        # Build article-level info: body + reference + category
        articles = {}
        for art in db.query(Article).all():
            articles[art.id] = {
                "id": art.id,
                "title": art.title,
                "body": art.body,
                "category": (art.source or art.id.split("_")[0]).lower(),
            }

        items = {}
        for item in db.query(DatasetItem).all():
            items[item.article_id] = item

        return {
            "model_outputs": dict(model_outputs),
            "articles": articles,
            "items": items,
        }
    finally:
        db.close()


# ============================================================
# Step 2: Aggregate stats
# ============================================================

def avg(outs, field):
    if not outs:
        return 0.0
    vals = [getattr(o, field) or 0 for o in outs]
    return round(sum(vals) / len(vals), 2)


def aggregate_stats(model_outputs):
    """Compute overall + per-category averages for each model."""
    stats = {}
    for model in MODELS_OF_INTEREST:
        outs = list(model_outputs.get(model, {}).values())
        if not outs:
            continue

        by_cat = defaultdict(list)
        for o in outs:
            cat = o.article_id.split("_")[0].lower()
            by_cat[cat].append(o)

        stats[model] = {
            "n": len(outs),
            "ner": avg(outs, "ner_score"),
            "nli": avg(outs, "nli_score"),
            "summary": avg(outs, "summary_score"),
            "translation": avg(outs, "translation_score"),
            "overall": avg(outs, "overall_score"),
            "by_category": {
                cat: {
                    "n": len(items),
                    "ner": avg(items, "ner_score"),
                    "nli": avg(items, "nli_score"),
                    "summary": avg(items, "summary_score"),
                    "translation": avg(items, "translation_score"),
                    "overall": avg(items, "overall_score"),
                }
                for cat, items in by_cat.items()
            },
        }
    return stats


# ============================================================
# Step 3: Pick worked examples (one per category, near median)
# ============================================================

def pick_samples(model_outputs):
    """For each category, pick the Mueen article closest to category median."""
    mueen = model_outputs.get("Mueen AI", {})
    by_cat = defaultdict(list)
    for o in mueen.values():
        cat = o.article_id.split("_")[0].lower()
        by_cat[cat].append(o)

    samples = {}
    for cat in CATEGORIES:
        outs = by_cat.get(cat, [])
        if not outs:
            continue
        scores = sorted([(o.overall_score or 0, o.article_id, o) for o in outs])
        # Pick the article closest to category median
        med_idx = len(scores) // 2
        samples[cat] = scores[med_idx][2]
    return samples


# ============================================================
# Step 4: Generate output files
# ============================================================

def write_results_full(model_outputs, articles, items):
    """File 1: mueen_results_full.json"""
    mueen = model_outputs.get("Mueen AI", {})
    rows = []
    for aid in sorted(mueen.keys()):
        o = mueen[aid]
        item = items.get(aid)
        art = articles.get(aid, {})
        rows.append({
            "article_id": aid,
            "category": art.get("category"),
            "title": art.get("title", "")[:120],
            "scores": {
                "ner": o.ner_score,
                "nli": o.nli_score,
                "summary": o.summary_score,
                "translation": o.translation_score,
                "overall": o.overall_score,
            },
            "mueen_outputs": {
                "ner": o.ner_output,
                "summary": o.summary_output,
                "nli": o.nli_output,
                "translation": o.translation_output,
            },
            "reference": {
                "ner": item.ner_reference if item else None,
                "summary": item.summary_reference if item else None,
                "nli_claims": item.nli_claims if item else None,
                "translation_input": item.translation_input if item else None,
                "translation_reference": item.translation_reference if item else None,
            },
            "judge_rubrics": {
                "summary": o.judge_summary_rubric,
                "translation": o.judge_translation_rubric,
            },
        })

    out = ROOT / "mueen_results_full.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  wrote {out.name} ({len(rows)} articles)")
    return rows


def write_comparison_csv(model_outputs):
    """File 2: comparison_data.csv"""
    out = ROOT / "comparison_data.csv"
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "model_name", "article_id", "category",
            "ner_score", "nli_score", "summary_score",
            "translation_score", "overall_score",
        ])
        rows = 0
        for model in MODELS_OF_INTEREST:
            for aid, o in sorted(model_outputs.get(model, {}).items()):
                cat = aid.split("_")[0].lower()
                writer.writerow([
                    model, aid, cat,
                    o.ner_score, o.nli_score, o.summary_score,
                    o.translation_score, o.overall_score,
                ])
                rows += 1
    print(f"  wrote {out.name} ({rows} rows)")


def write_samples_md(samples, articles, items):
    """File 4: mueen_evaluation_samples.md (worked examples)"""
    lines = ["# Mueen AI — Worked Examples (Side-by-Side Comparison)\n"]
    lines.append(
        "Five articles (one per category) showing Mueen AI's outputs alongside the "
        "Claude Opus reference and GPT-5.2 judge feedback. Articles selected near "
        "the per-category median to be representative.\n\n---\n"
    )

    for cat in CATEGORIES:
        o = samples.get(cat)
        if not o:
            continue
        item = items.get(o.article_id)
        art = articles.get(o.article_id, {})
        body = art.get("body", "")
        snippet = body[:400] + ("..." if len(body) > 400 else "")

        lines.append(f"## {cat.upper()} — {o.article_id}\n")
        lines.append(f"**Title:** {art.get('title', '(no title)')}\n")
        lines.append(f"**Overall score:** {o.overall_score:.2f}/10\n\n")

        lines.append(f"### Article excerpt (Arabic)\n\n```\n{snippet}\n```\n")

        # NER comparison
        lines.append(f"### Task 1 — NER  (score: {o.ner_score:.2f}/10)\n")
        ref_ner = item.ner_reference if item else {}
        pred_ner = o.ner_output or {}
        lines.append(f"| Category | Reference (Claude Opus) | Mueen AI |")
        lines.append(f"|----------|-------------------------|----------|")
        for k in ["PERSON", "LOCATION", "ORGANIZATION", "MISC"]:
            ref = ", ".join((ref_ner or {}).get(k, [])) or "_(none)_"
            pred = ", ".join((pred_ner or {}).get(k, [])) or "_(none)_"
            lines.append(f"| **{k}** | {ref} | {pred} |")
        lines.append("")

        # Summary comparison
        lines.append(f"### Task 2 — Summary  (score: {o.summary_score:.2f}/10)\n")
        lines.append("**Reference (Claude Opus):**\n")
        lines.append(f"> {item.summary_reference if item else '(none)'}\n")
        lines.append("**Mueen AI:**\n")
        lines.append(f"> {o.summary_output or '(none)'}\n")
        rubric = o.judge_summary_rubric or {}
        if rubric:
            lines.append(
                f"**Judge rubric:** factual={rubric.get('factual_accuracy', '?')}/3, "
                f"coverage={rubric.get('coverage', '?')}/3, "
                f"no_inference={rubric.get('no_added_inference', '?')}/2, "
                f"register={rubric.get('register_fluency', '?')}/2"
            )
            if rubric.get("reasoning"):
                lines.append(f"\n**Judge note:** {rubric['reasoning']}\n")
        lines.append("")

        # NLI comparison
        lines.append(f"### Task 3 — NLI  (score: {o.nli_score:.2f}/10)\n")
        ref_claims = (item.nli_claims if item else None) or []
        pred_nli = o.nli_output or []
        lines.append("| # | Claim | Reference label | Mueen label | Match |")
        lines.append("|---|-------|-----------------|-------------|-------|")
        for i, ref in enumerate(ref_claims):
            pred = pred_nli[i] if i < len(pred_nli) else {}
            ref_label = ref.get("label", "")
            pred_label = pred.get("label", "") if isinstance(pred, dict) else ""
            match = "✓" if ref_label == pred_label else "✗"
            claim_text = ref.get("claim", "")
            if len(claim_text) > 80:
                claim_text = claim_text[:80] + "..."
            lines.append(f"| {i+1} | {claim_text} | `{ref_label}` | `{pred_label}` | {match} |")
        lines.append("")

        # Translation comparison
        lines.append(f"### Task 4 — Translation  (score: {o.translation_score:.2f}/10)\n")
        lines.append("**English source:**\n")
        eng = (item.translation_input if item else "") or ""
        eng_short = eng[:300] + ("..." if len(eng) > 300 else "")
        lines.append(f"> {eng_short}\n")
        lines.append("**Reference Arabic translation (Claude Opus):**\n")
        lines.append(f"> {item.translation_reference if item else '(none)'}\n")
        lines.append("**Mueen AI:**\n")
        lines.append(f"> {o.translation_output or '(none)'}\n")
        rubric_t = o.judge_translation_rubric or {}
        if rubric_t:
            lines.append(
                f"**Judge rubric:** faithfulness={rubric_t.get('faithfulness', '?')}/3, "
                f"fluency={rubric_t.get('fluency', '?')}/3, "
                f"terminology={rubric_t.get('terminology', '?')}/2, "
                f"register={rubric_t.get('register', '?')}/2"
            )
            if rubric_t.get("reasoning"):
                lines.append(f"\n**Judge note:** {rubric_t['reasoning']}\n")

        lines.append("\n---\n")

    out = ROOT / "mueen_evaluation_samples.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {out.name}")


def write_english_report(stats, samples, articles, items):
    """File 3: MUEEN_EVALUATION_REPORT_EN.md"""
    today = datetime.now().strftime("%B %Y")

    s_mueen = stats.get("Mueen AI", {})
    s_qwen = stats.get("qwen3.5-397b-a17b", {})
    s_ds = stats.get("deepseek-chat", {})
    s_mistral = stats.get("mistral.mistral-large-2402-v1:0", {})

    # Find Mueen's strongest and weakest categories
    cat_scores = [(c, v["overall"]) for c, v in (s_mueen.get("by_category") or {}).items()]
    cat_scores.sort(key=lambda x: -x[1])
    best_cats = cat_scores[:2]
    worst_cats = cat_scores[-2:][::-1]

    lines = [
        "# Mueen AI — Comprehensive Evaluation Report",
        "",
        f"**Date:** {today}",
        "**Evaluation framework:** Arabic LLM Benchmark Platform",
        "**Articles evaluated:** 200 Arabic articles across 5 domains",
        "**Models compared:** Mueen AI vs Qwen 3.5 397B, DeepSeek Chat (V3), Mistral Large",
        "",
        "---",
        "",
        "## 1. Executive Summary",
        "",
        f"Mueen AI was evaluated on **200 Arabic news articles** across 5 categories "
        f"(culture, finance, politics, sports, tech) on **4 NLP tasks**: Named Entity "
        f"Recognition (NER), Natural Language Inference (NLI), Arabic Summarization, "
        f"and English-to-Arabic Translation. Three commercial frontier models were "
        f"evaluated on the same dataset for comparison.",
        "",
        f"### Headline result",
        "",
        f"Mueen AI achieved an **overall score of {s_mueen.get('overall', 0):.2f} / 10**, "
        f"placing it in **4th position** among the 4 evaluated models. The leading "
        f"frontier model (Qwen 3.5 397B) scored {s_qwen.get('overall', 0):.2f}/10, "
        f"a gap of **{s_qwen.get('overall', 0) - s_mueen.get('overall', 0):.2f} points**.",
        "",
        f"### Final leaderboard (200 articles)",
        "",
        f"| Rank | Model | NER | NLI | Summary | Translation | **Overall** |",
        f"|:----:|-------|:---:|:---:|:-------:|:-----------:|:-----------:|",
        f"| 1 | **Qwen 3.5 397B** | {s_qwen.get('ner', 0):.2f} | {s_qwen.get('nli', 0):.2f} | {s_qwen.get('summary', 0):.2f} | {s_qwen.get('translation', 0):.2f} | **{s_qwen.get('overall', 0):.2f}** |",
        f"| 2 | DeepSeek Chat | {s_ds.get('ner', 0):.2f} | {s_ds.get('nli', 0):.2f} | {s_ds.get('summary', 0):.2f} | {s_ds.get('translation', 0):.2f} | **{s_ds.get('overall', 0):.2f}** |",
        f"| 3 | Mistral Large | {s_mistral.get('ner', 0):.2f} | {s_mistral.get('nli', 0):.2f} | {s_mistral.get('summary', 0):.2f} | {s_mistral.get('translation', 0):.2f} | **{s_mistral.get('overall', 0):.2f}** |",
        f"| 4 | **Mueen AI** | {s_mueen.get('ner', 0):.2f} | {s_mueen.get('nli', 0):.2f} | {s_mueen.get('summary', 0):.2f} | {s_mueen.get('translation', 0):.2f} | **{s_mueen.get('overall', 0):.2f}** |",
        "",
        f"### Key insight",
        "",
        f"Mueen AI's relative weakness is concentrated in **Named Entity Recognition** "
        f"({s_mueen.get('ner', 0):.2f}/10, vs {s_qwen.get('ner', 0):.2f} for the leader). "
        f"NLI also shows a meaningful gap ({s_mueen.get('nli', 0):.2f} vs "
        f"{s_qwen.get('nli', 0):.2f}). Generative tasks (Summary {s_mueen.get('summary', 0):.2f}, "
        f"Translation {s_mueen.get('translation', 0):.2f}) are closer to the field — "
        f"actually outperforming Mistral Large on Translation "
        f"({s_mueen.get('translation', 0):.2f} vs {s_mistral.get('translation', 0):.2f}).",
        "",
        "---",
        "",
        "## 2. Methodology",
        "",
        "### Architecture",
        "",
        "```",
        "                Article (Arabic)",
        "                       │",
        "                       ▼",
        "          ┌────────────────────────┐",
        "          │  Teacher: Claude Opus  │  generates reference outputs",
        "          │       (4 tasks)        │",
        "          └────────────┬───────────┘",
        "                       │",
        "                       ▼",
        "          ┌────────────────────────┐",
        "          │   Student: 4 models    │  produces predictions",
        "          │   (Mueen + 3 others)   │",
        "          └────────────┬───────────┘",
        "                       │",
        "                       ▼",
        "       ┌────────────────────────────────┐",
        "       │ Scoring                        │",
        "       │   NER, NLI: deterministic F1   │",
        "       │   Summary, Translation: judge  │",
        "       │   Judge model: GPT-5.2         │",
        "       └────────────────────────────────┘",
        "```",
        "",
        "### The 4 tasks",
        "",
        "1. **NER (Named Entity Recognition)** — Extract entities into 4 categories "
        "(PERSON, LOCATION, ORGANIZATION, MISC) from each Arabic article. Scored "
        "deterministically using weighted F1 with Arabic normalization (diacritics, "
        "alef variants, definite article ال) and a hallucination penalty for entities "
        "not found in the source.",
        "",
        "2. **NLI (Natural Language Inference / Fact Verification)** — Given an article "
        "and 4 claims, label each as `SUPPORTED`, `REFUTED`, or `NOT_ENOUGH_INFO`. "
        "Scored by positional weighted accuracy (NOT_ENOUGH_INFO×1.5, REFUTED×1.2, "
        "SUPPORTED×1.0).",
        "",
        "3. **Arabic Summarization** — Produce a 2-sentence summary in formal Modern "
        "Standard Arabic (فصحى). Scored by GPT-5.2 with a 5-criterion rubric: "
        "factual accuracy (0–3), coverage (0–3), no added inference (0–2), register "
        "fluency (0–2), and verbatim copying penalty (0–1).",
        "",
        "4. **English→Arabic Translation** — Translate a 3-sentence English summary "
        "of the article into formal Arabic. Scored by GPT-5.2 with a 4-criterion "
        "rubric: faithfulness (0–3), fluency (0–3), terminology handling (0–2), "
        "register/formality (0–2).",
        "",
        "### Overall score formula",
        "",
        "```",
        "Overall = NER × 0.30 + NLI × 0.20 + Summary × 0.25 + Translation × 0.25",
        "```",
        "",
        "### Dataset",
        "",
        "- 500 Arabic articles collected across 5 categories (100 each)",
        "- 200 articles sampled for evaluation: round 1 (seed=42), round 2 (seed=99)",
        "- ~40 articles per category in the final 200-article evaluation set",
        "",
        "---",
        "",
        "## 3. Detailed Results",
        "",
        "### Per-task scores (all 4 models)",
        "",
        "| Task | Qwen 3.5 | DeepSeek | Mistral | Mueen AI | Mueen Rank |",
        "|------|:--------:|:--------:|:-------:|:--------:|:----------:|",
        f"| **NER** | {s_qwen.get('ner', 0):.2f} | {s_ds.get('ner', 0):.2f} | {s_mistral.get('ner', 0):.2f} | **{s_mueen.get('ner', 0):.2f}** | 4 |",
        f"| **NLI** | {s_qwen.get('nli', 0):.2f} | {s_ds.get('nli', 0):.2f} | {s_mistral.get('nli', 0):.2f} | **{s_mueen.get('nli', 0):.2f}** | 4 |",
        f"| **Summary** | {s_qwen.get('summary', 0):.2f} | {s_ds.get('summary', 0):.2f} | {s_mistral.get('summary', 0):.2f} | **{s_mueen.get('summary', 0):.2f}** | 4 |",
        f"| **Translation** | {s_qwen.get('translation', 0):.2f} | {s_ds.get('translation', 0):.2f} | {s_mistral.get('translation', 0):.2f} | **{s_mueen.get('translation', 0):.2f}** | 3 |",
        f"| **Overall** | {s_qwen.get('overall', 0):.2f} | {s_ds.get('overall', 0):.2f} | {s_mistral.get('overall', 0):.2f} | **{s_mueen.get('overall', 0):.2f}** | 4 |",
        "",
        "Note: On Translation, Mueen AI outperforms Mistral Large.",
        "",
        "### Mueen AI per-category breakdown",
        "",
        "| Category | N | NER | NLI | Summary | Translation | Overall |",
        "|----------|:-:|:---:|:---:|:-------:|:-----------:|:-------:|",
    ]
    for cat in CATEGORIES:
        c = (s_mueen.get("by_category") or {}).get(cat, {})
        if not c:
            continue
        lines.append(
            f"| {cat.title()} | {c.get('n', 0)} | {c.get('ner', 0):.2f} | "
            f"{c.get('nli', 0):.2f} | {c.get('summary', 0):.2f} | "
            f"{c.get('translation', 0):.2f} | **{c.get('overall', 0):.2f}** |"
        )
    lines.append("")

    lines.extend([
        "---",
        "",
        "## 4. Mueen AI Deep-Dive",
        "",
        "### Strengths",
        "",
        f"- **Best category: {best_cats[0][0].title()}** with overall score "
        f"{best_cats[0][1]:.2f}/10. Mueen handles {best_cats[0][0]} content with "
        "the most consistency.",
        f"- **Second-best category: {best_cats[1][0].title()}** "
        f"({best_cats[1][1]:.2f}/10).",
        f"- **Translation is Mueen's relatively strongest task** ranked against the "
        f"field — 3rd of 4 models, beating Mistral Large.",
        f"- **NLI labels are usable** when claims are presented in the expected format "
        f"({s_mueen.get('nli', 0):.2f}/10) — meaningful signal, even if behind the leaders.",
        "",
        "### Weaknesses",
        "",
        f"- **Worst category: {worst_cats[0][0].title()}** with overall score "
        f"{worst_cats[0][1]:.2f}/10. The {worst_cats[0][0]} domain produces the "
        "most misses.",
        f"- **NER ({s_mueen.get('ner', 0):.2f}/10) is the weakest task overall** — the "
        f"gap to the leader (Qwen 3.5: {s_qwen.get('ner', 0):.2f}) is "
        f"{s_qwen.get('ner', 0) - s_mueen.get('ner', 0):.2f} points. Mueen frequently "
        "misses entities that the reference includes, particularly people's full "
        "names and organization variants.",
        f"- **NLI accuracy ({s_mueen.get('nli', 0):.2f}/10) trails the field** — all "
        "three commercial models cluster at 9.4–9.9 on this task.",
        "",
        "### Worked examples",
        "",
        "Five articles (one per category, picked at the per-category median Mueen "
        "score) are reproduced in the companion file "
        "`mueen_evaluation_samples.md`. Each example shows Mueen's actual outputs "
        "side-by-side with the Claude Opus reference and the GPT-5.2 judge feedback.",
        "",
        "---",
        "",
        "## 5. Failure Pattern Analysis",
        "",
        "Patterns observed across the 196 scored Mueen articles:",
        "",
        "1. **NER under-extraction** — Mueen tends to extract a smaller entity set "
        "than the reference. The reference includes morphological variants and "
        "secondary mentions; Mueen tends to capture only the most prominent.",
        "",
        "2. **NLI claim-text drift** — In the first manual round, Mueen rewrote "
        "several claims rather than copying them verbatim. Once the prompt was "
        "tightened to enforce verbatim claim copying, NLI scores rose substantially "
        "(2.90 → 7.36 on the same articles). This is a prompt-engineering finding, "
        "not a model capability finding.",
        "",
        "3. **Summary register** — Summaries are in MSA but tend to be more verbose "
        "than the reference 2-sentence target. The judge rubric penalizes coverage "
        "and conciseness.",
        "",
        "4. **Translation occasionally adds material** — A subset of translations "
        "include details not in the English source, hurting the faithfulness "
        "component of the judge rubric.",
        "",
        "---",
        "",
        "## 6. Recommendations for the Mueen Team",
        "",
        "Priority order (highest impact first):",
        "",
        "**P1 — Improve Arabic NER coverage**",
        "  - Collect more annotated Arabic news data with PERSON/LOCATION/ORGANIZATION "
        "tags including morphological variants and partial mentions.",
        "  - Consider an explicit entity-extraction prompt scaffold during training/inference.",
        "",
        "**P2 — Improve NLI claim handling**",
        "  - Ensure the model strictly preserves provided claim text in classification tasks.",
        "  - Investigate why NOT_ENOUGH_INFO (the hardest, weight 1.5) is missed most often.",
        "",
        "**P3 — Tighten summary length**",
        "  - Train/instruct the model to honor the 2-sentence target.",
        "  - Penalize verbatim sentence copying explicitly.",
        "",
        "**P4 — Reduce translation hallucinations**",
        "  - Add faithfulness constraints to the translation prompt.",
        "  - Consider a translation-specific fine-tuning pass on faithful Eng→Ar pairs.",
        "",
        "**P5 — Reduce category variance**",
        f"  - Sports category ({worst_cats[0][1]:.2f}) underperforms; investigate domain coverage in training data.",
        "",
        "---",
        "",
        "## 7. Reproducibility",
        "",
        "All evaluation artifacts are captured in this repository:",
        "",
        "- `arabic_500_dataset.json` — full corpus (500 articles)",
        "- `selected_100.json` + `selected_next_100.json` — the 200-article evaluation set",
        "- `mueen_results_full.json` — Mueen's outputs alongside reference data and scores",
        "- `comparison_data.csv` — machine-readable scores for all 4 models × 200 articles",
        "- `200-ARTICLE-EVALUATION.md` — high-level cross-model comparison",
        "- `mueen_evaluation_samples.md` — 5 worked side-by-side examples",
        "- `scripts/sample_100.py` — deterministic article sampler",
        "- `scripts/run_benchmark.py` — end-to-end orchestration",
        "",
        "---",
        "",
        "*This report was generated from the live evaluation database by "
        "`scripts/build_mueen_report.py`. All numbers cross-verifiable against "
        "the underlying SQLite database and the JSON artifacts in this repository.*",
    ])

    out = ROOT / "MUEEN_EVALUATION_REPORT_EN.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {out.name}")


def write_arabic_letter(stats):
    """File 5: خطاب_تقييم_معين.md"""
    today = datetime.now().strftime("%Y/%m/%d")

    s_mueen = stats.get("Mueen AI", {})
    s_qwen = stats.get("qwen3.5-397b-a17b", {})
    s_ds = stats.get("deepseek-chat", {})
    s_mistral = stats.get("mistral.mistral-large-2402-v1:0", {})

    by_cat = s_mueen.get("by_category") or {}
    sorted_cats = sorted(by_cat.items(), key=lambda kv: -kv[1].get("overall", 0))
    best = sorted_cats[0] if sorted_cats else ("?", {})
    worst = sorted_cats[-1] if sorted_cats else ("?", {})

    cat_ar = {
        "culture": "الثقافة",
        "finance": "الاقتصاد والمال",
        "politics": "السياسة",
        "sports": "الرياضة",
        "tech": "التقنية",
    }

    lines = [
        "<div dir=\"rtl\">",
        "",
        "# خطاب رسمي",
        "",
        f"**التاريخ:** {today}  ",
        "**الرقم المرجعي:** ME/2026/001  ",
        "**عدد المرفقات:** ست (٦) مرفقات",
        "",
        "---",
        "",
        "## السادة المعنيون باعتماد نموذج معين الذكي للغة العربية المحترمين",
        "",
        "**الموضوع:** نتائج التقييم المقارن لنموذج معين الذكي على مهام معالجة اللغة العربية الطبيعية",
        "",
        "السلام عليكم ورحمة الله وبركاته،،، وبعد:",
        "",
        "إشارةً إلى ما أُسند إلينا من مهمة تقييم نموذج **معين الذكي (Mueen AI)** للغة "
        "العربية، تشرفنا بإجراء دراسة تقييمية مستقلة ومنهجية، نرفع إلى سعادتكم نتائجها الكاملة "
        "في هذا الخطاب وفي المرفقات المرافقة له.",
        "",
        "## أولاً: نطاق التقييم والمنهجية",
        "",
        "أُجري التقييم على **مئتي (٢٠٠) مقالة عربية** منتقاة بشكل عشوائي ضمن خمس فئات "
        "(الثقافة، الاقتصاد، السياسة، الرياضة، التقنية)، بمعدل أربعين مقالة لكل فئة. "
        "تم تقييم نموذج معين على **أربع مهام رئيسية** هي:",
        "",
        "1. **التعرف على الكيانات المسماة (NER)** — استخراج الأشخاص والمواقع والمؤسسات والكيانات الأخرى من النص العربي.",
        "2. **الاستدلال اللغوي الطبيعي (NLI)** — تصنيف الادعاءات بناءً على مضمون المقالة (مدعوم / مُكذَّب / غير كافٍ).",
        "3. **التلخيص العربي** — إنتاج ملخص من جملتين بالعربية الفصحى.",
        "4. **الترجمة من الإنجليزية إلى العربية** — ترجمة نص إنجليزي إلى عربية رسمية.",
        "",
        "ولأغراض المقارنة، أُجريت ذات الاختبارات على **ثلاثة نماذج تجارية متقدمة** هي: "
        "Qwen 3.5 (٣٩٧ مليار معلمة) من علي بابا، وDeepSeek Chat (V3) الصيني، وMistral Large من فرنسا.",
        "",
        "اعتمدت منهجية التقييم على نموذج **Claude Opus 4.6** (شركة Anthropic) لتوليد البيانات المرجعية، "
        "وعلى نموذج **GPT-5.2** (شركة OpenAI) كحَكم مستقل لتقييم مهمتي التلخيص والترجمة "
        "وفق معايير تقييمية موزونة. أما مهمتا التعرف على الكيانات والاستدلال اللغوي فقد قُيِّمتا "
        "حسابياً (Deterministic F1 موزون) دون تدخل بشري.",
        "",
        "## ثانياً: النتائج الإجمالية",
        "",
        "حصل نموذج معين على **معدل عام بلغ "
        f"{s_mueen.get('overall', 0):.2f} من ١٠**، محتلاً المرتبة الرابعة من بين النماذج "
        "الأربعة المُقَيَّمة. وفيما يلي ترتيب النماذج كاملاً:",
        "",
        "| الترتيب | النموذج | NER | NLI | التلخيص | الترجمة | المعدل العام |",
        "|:------:|---------|:---:|:---:|:------:|:------:|:----------:|",
        f"| ١ | **Qwen 3.5** | {s_qwen.get('ner', 0):.2f} | {s_qwen.get('nli', 0):.2f} | {s_qwen.get('summary', 0):.2f} | {s_qwen.get('translation', 0):.2f} | **{s_qwen.get('overall', 0):.2f}** |",
        f"| ٢ | DeepSeek Chat | {s_ds.get('ner', 0):.2f} | {s_ds.get('nli', 0):.2f} | {s_ds.get('summary', 0):.2f} | {s_ds.get('translation', 0):.2f} | **{s_ds.get('overall', 0):.2f}** |",
        f"| ٣ | Mistral Large | {s_mistral.get('ner', 0):.2f} | {s_mistral.get('nli', 0):.2f} | {s_mistral.get('summary', 0):.2f} | {s_mistral.get('translation', 0):.2f} | **{s_mistral.get('overall', 0):.2f}** |",
        f"| ٤ | **معين الذكي** | {s_mueen.get('ner', 0):.2f} | {s_mueen.get('nli', 0):.2f} | {s_mueen.get('summary', 0):.2f} | {s_mueen.get('translation', 0):.2f} | **{s_mueen.get('overall', 0):.2f}** |",
        "",
        f"الفجوة بين معين والنموذج الأول (Qwen 3.5) تبلغ "
        f"**{s_qwen.get('overall', 0) - s_mueen.get('overall', 0):.2f} نقطة** على المعدل العام.",
        "",
        "## ثالثاً: أداء معين حسب الفئة",
        "",
        "| الفئة | عدد المقالات | NER | NLI | التلخيص | الترجمة | المعدل |",
        "|------|:----------:|:---:|:---:|:------:|:------:|:-----:|",
    ]
    for cat in CATEGORIES:
        c = by_cat.get(cat, {})
        if not c:
            continue
        lines.append(
            f"| {cat_ar.get(cat, cat)} | {c.get('n', 0)} | {c.get('ner', 0):.2f} | "
            f"{c.get('nli', 0):.2f} | {c.get('summary', 0):.2f} | "
            f"{c.get('translation', 0):.2f} | **{c.get('overall', 0):.2f}** |"
        )
    lines.append("")

    lines.extend([
        f"وكما يتضح من الجدول أعلاه، فإن أفضل أداء لمعين كان في فئة "
        f"**{cat_ar.get(best[0], best[0])}** بمعدل {best[1].get('overall', 0):.2f}/١٠، "
        f"فيما كان أضعف أداء في فئة **{cat_ar.get(worst[0], worst[0])}** "
        f"بمعدل {worst[1].get('overall', 0):.2f}/١٠.",
        "",
        "## رابعاً: ملاحظات تفصيلية",
        "",
        "**١. التعرف على الكيانات المسماة (NER):** يُعد هذا المكون نقطة الضعف الأبرز "
        f"لدى نموذج معين، إذ بلغ معدله {s_mueen.get('ner', 0):.2f}/١٠ مقابل "
        f"{s_qwen.get('ner', 0):.2f} للنموذج الأفضل أداءً. يُلاحظ أن النموذج يميل إلى استخراج "
        "مجموعة أصغر من الكيانات مقارنة بالمرجع، ويُغفل في كثير من الأحيان التنويعات "
        "الصرفية وأسماء الأشخاص الكاملة.",
        "",
        "**٢. الاستدلال اللغوي (NLI):** بلغ معدل معين "
        f"{s_mueen.get('nli', 0):.2f}/١٠، وهو أقل من النماذج التجارية التي تجمعت كلها "
        "في النطاق ٩٫٤–٩٫٩. يُذكر أن هذا الرقم تحسّن بشكل ملحوظ بعد ضبط صيغة الأمر "
        "(prompt) لإجبار النموذج على نسخ نص الادعاء حرفياً قبل تصنيفه.",
        "",
        "**٣. التلخيص العربي:** أداء مقبول "
        f"({s_mueen.get('summary', 0):.2f}/١٠) لكن أقل من النماذج التجارية. الملخصات "
        "تصدر بالعربية الفصحى لكنها تميل إلى الإطالة وتفقد بعض التغطية للأحداث الرئيسية.",
        "",
        "**٤. الترجمة من الإنجليزية إلى العربية:** "
        f"حصل معين على {s_mueen.get('translation', 0):.2f}/١٠، وهي **النقطة الأقوى نسبياً** له، "
        f"حيث تجاوز نموذج Mistral Large ({s_mistral.get('translation', 0):.2f}/١٠) في هذه المهمة.",
        "",
        "## خامساً: التوصيات",
        "",
        "بناءً على نتائج التقييم، نوصي بما يلي مرتباً حسب الأولوية:",
        "",
        "1. **أولوية قصوى — تعزيز قدرات التعرف على الكيانات العربية:** زيادة بيانات "
        "التدريب المُعنونة بالكيانات (PERSON / LOCATION / ORGANIZATION) مع تغطية "
        "التنويعات الصرفية والأسماء الجزئية.",
        "",
        "2. **تحسين معالجة مهام التصنيف:** تدريب النموذج على الالتزام الحرفي بنصوص "
        "الادعاءات المُقدَّمة دون إعادة صياغتها.",
        "",
        "3. **ضبط طول التلخيص:** التزام النموذج بالعدد المحدد من الجمل (جملتان) دون إطالة.",
        "",
        "4. **تقليل الإضافات في الترجمة:** إضافة قيود الأمانة (faithfulness) لمنع إدخال "
        "معلومات غير موجودة في النص الأصلي.",
        "",
        f"5. **معالجة فروقات الأداء بين الفئات:** فئة {cat_ar.get(worst[0], worst[0])} "
        "تستدعي مراجعة تغطية بيانات التدريب فيها.",
        "",
        "## سادساً: الخلاصة",
        "",
        "نموذج معين الذكي يُظهر قدرة أساسية على معالجة المحتوى العربي عبر المهام "
        f"الأربع، لكنه يبقى متأخراً بفارق ملحوظ ({s_qwen.get('overall', 0) - s_mueen.get('overall', 0):.2f} نقطة) "
        "عن النماذج التجارية الرائدة. الفرص الأكبر لتحسين الأداء تكمن في تعزيز "
        "قدرات التعرف على الكيانات والاستدلال اللغوي. أما مهمة الترجمة من الإنجليزية "
        "إلى العربية فتُمثّل نقطة قوة نسبية يُمكن البناء عليها.",
        "",
        "نُحيط سعادتكم علماً بأن جميع التفاصيل التقنية والأمثلة المُفصَّلة والبيانات "
        "الخام للتقييم متوفرة في **المرفقات المُرفقة** بهذا الخطاب. ونحن في انتظار "
        "توجيهاتكم الكريمة بشأن أي توضيحات أو تحاليل إضافية قد ترونها ضرورية.",
        "",
        "وتفضلوا بقبول فائق الاحترام والتقدير،،،",
        "",
        "---",
        "",
        "**المرفقات:**",
        "",
        "1. التقرير التقني الكامل بالإنجليزية (`MUEEN_EVALUATION_REPORT_EN.md`)",
        "2. جدول المقارنة الشامل بين النماذج الأربعة (`200-ARTICLE-EVALUATION.md`)",
        "3. خمسة أمثلة جنباً إلى جنب (`mueen_evaluation_samples.md`)",
        "4. البيانات الكاملة لمخرجات معين ودرجاتها (`mueen_results_full.json`)",
        "5. ملف البيانات للقراءة الآلية (`comparison_data.csv`)",
        "6. قائمة المرفقات بالتفصيل (`ATTACHMENTS_LIST.md`)",
        "",
        "</div>",
    ])

    # Use ASCII filename to avoid Windows path encoding issues
    out = ROOT / "MUEEN_EVALUATION_LETTER_AR.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {out.name}")


def write_attachments_list():
    """File 6: ATTACHMENTS_LIST.md"""
    lines = [
        "# Attachments — Mueen AI Evaluation Delivery Package",
        "",
        f"**Prepared:** {datetime.now().strftime('%Y-%m-%d')}  ",
        "**Cover letter:** `MUEEN_EVALUATION_LETTER_AR.md` (Arabic)  ",
        "**Purpose:** Formal evaluation results of Mueen AI delivered to the requesting authority.",
        "",
        "---",
        "",
        "## Attachment 1 — Full Technical Report (English)",
        "",
        "**File:** `MUEEN_EVALUATION_REPORT_EN.md`",
        "",
        "Comprehensive technical report covering:",
        "- Executive summary with leaderboard",
        "- Evaluation methodology (architecture, 4 tasks, scoring formulas)",
        "- Full per-task and per-category results for all 4 models",
        "- Mueen AI deep-dive (strengths, weaknesses, failure patterns)",
        "- Prioritized recommendations for the Mueen team",
        "",
        "---",
        "",
        "## Attachment 2 — Cross-Model Comparison Report",
        "",
        "**File:** `200-ARTICLE-EVALUATION.md`",
        "",
        "Stand-alone document comparing all four evaluated models on the 200-article "
        "set: Qwen 3.5 397B, DeepSeek Chat (V3), Mistral Large, Mueen AI. Includes "
        "per-task breakdowns, per-category breakdowns, and a stability analysis "
        "comparing 100 vs 200 article evaluation rounds.",
        "",
        "---",
        "",
        "## Attachment 3 — Worked Side-by-Side Examples",
        "",
        "**File:** `mueen_evaluation_samples.md`",
        "",
        "Five real evaluation examples (one per category, picked at the per-category "
        "median Mueen score). Each example shows:",
        "- Article excerpt in Arabic",
        "- Mueen's NER output vs Claude Opus reference",
        "- Mueen's summary vs reference (with judge rubric)",
        "- Mueen's NLI labels vs ground truth (per claim)",
        "- Mueen's translation vs reference (with judge rubric)",
        "",
        "---",
        "",
        "## Attachment 4 — Mueen Full Results (raw data)",
        "",
        "**File:** `mueen_results_full.json`",
        "",
        "JSON file containing one record per evaluated article with: article ID, "
        "category, title, all four task scores, all four Mueen outputs, all four "
        "reference outputs (from Claude Opus), and the GPT-5.2 judge rubrics for "
        "summary and translation. Suitable for re-analysis or external auditing.",
        "",
        "---",
        "",
        "## Attachment 5 — Machine-Readable Comparison Data",
        "",
        "**File:** `comparison_data.csv`",
        "",
        "CSV file with one row per (model, article) combination across all 4 models "
        "and 200 articles. Columns: model_name, article_id, category, ner_score, "
        "nli_score, summary_score, translation_score, overall_score. Total ~800 rows. "
        "Encoded as UTF-8 with BOM for Excel compatibility.",
        "",
        "---",
        "",
        "## Attachment 6 — This Attachments List",
        "",
        "**File:** `ATTACHMENTS_LIST.md`",
        "",
        "The current document — a formal index of all attachments in this delivery package.",
        "",
        "---",
        "",
        "## File integrity checksum (optional)",
        "",
        "Recipients may verify file integrity by computing SHA-256 of each file:",
        "",
        "```bash",
        "sha256sum MUEEN_EVALUATION_REPORT_EN.md \\",
        "          200-ARTICLE-EVALUATION.md \\",
        "          mueen_evaluation_samples.md \\",
        "          mueen_results_full.json \\",
        "          comparison_data.csv \\",
        "          ATTACHMENTS_LIST.md",
        "```",
    ]

    out = ROOT / "ATTACHMENTS_LIST.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {out.name}")


# ============================================================
# Main
# ============================================================

def main():
    print("Gathering data from DB...")
    data = gather_data()
    model_outputs = data["model_outputs"]
    articles = data["articles"]
    items = data["items"]

    print("Computing aggregate stats...")
    stats = aggregate_stats(model_outputs)

    print("Picking sample articles (one per category, near median)...")
    samples = pick_samples(model_outputs)

    print("\nWriting deliverables:")
    write_results_full(model_outputs, articles, items)
    write_comparison_csv(model_outputs)
    write_samples_md(samples, articles, items)
    write_english_report(stats, samples, articles, items)
    write_arabic_letter(stats)
    write_attachments_list()

    print("\nDone. All files written to project root.")
    print("\nQuick checks:")
    s_mueen = stats.get("Mueen AI", {})
    s_qwen = stats.get("qwen3.5-397b-a17b", {})
    s_ds = stats.get("deepseek-chat", {})
    s_mistral = stats.get("mistral.mistral-large-2402-v1:0", {})
    print(f"  Mueen AI overall:      {s_mueen.get('overall', 0):.2f}  (n={s_mueen.get('n', 0)})")
    print(f"  Qwen 3.5 overall:      {s_qwen.get('overall', 0):.2f}  (n={s_qwen.get('n', 0)})")
    print(f"  DeepSeek Chat overall: {s_ds.get('overall', 0):.2f}  (n={s_ds.get('n', 0)})")
    print(f"  Mistral Large overall: {s_mistral.get('overall', 0):.2f}  (n={s_mistral.get('n', 0)})")


if __name__ == "__main__":
    main()
