"""Compute non-parametric bootstrap 95% confidence intervals for the
per-model scores on the 200-article evaluation.

Resamples articles (with replacement) 1000 times and computes the resulting
distribution of mean scores per model per task. Writes results to
`bootstrap_ci.json` for use in the report tables.

Run from project root:
    py scripts/compute_bootstrap_ci.py [--iters 1000] [--seed 11]
"""

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from database import SessionLocal
from models import (
    EvaluationRun, ModelOutput,
    RunStatus, OutputStatus,
)


MODELS = [
    "qwen3.5-397b-a17b",
    "deepseek-chat",
    "mistral.mistral-large-2402-v1:0",
    "Mueen AI",
]
MODEL_DISPLAY = {
    "qwen3.5-397b-a17b": "Qwen 3.5 397B",
    "deepseek-chat": "DeepSeek Chat",
    "mistral.mistral-large-2402-v1:0": "Mistral Large",
    "Mueen AI": "Mueen AI",
}
TASKS = ["ner_score", "nli_score", "summary_score", "translation_score", "overall_score"]


def gather():
    """model -> {article_id: {task: score}}"""
    db = SessionLocal()
    try:
        runs = db.query(EvaluationRun).filter(
            EvaluationRun.status == RunStatus.COMPLETED
        ).all()
        out = defaultdict(dict)
        for r in runs:
            outs = db.query(ModelOutput).filter(
                ModelOutput.run_id == r.id,
                ModelOutput.status == OutputStatus.SCORED,
            ).all()
            for o in outs:
                if o.article_id.startswith("ART_"):
                    continue
                prev = out[r.model_name].get(o.article_id)
                this_payload = {
                    "ner_score": o.ner_score,
                    "nli_score": o.nli_score,
                    "summary_score": o.summary_score,
                    "translation_score": o.translation_score,
                    "overall_score": o.overall_score,
                    "_processed_at": o.processed_at,
                }
                if prev is None or (
                    o.processed_at and prev.get("_processed_at")
                    and o.processed_at > prev["_processed_at"]
                ):
                    out[r.model_name][o.article_id] = this_payload
        return dict(out)
    finally:
        db.close()


def bootstrap_ci(values, iters, seed):
    """Returns (point_estimate, low_2.5%, high_97.5%) on the mean."""
    if not values:
        return None, None, None
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(iters):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(0.025 * iters)]
    hi = means[int(0.975 * iters) - 1]
    point = sum(values) / n
    return round(point, 3), round(lo, 3), round(hi, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=11)
    args = ap.parse_args()

    print(f"Loading scored outputs from DB...")
    data = gather()

    print(f"Bootstrap: {args.iters} iters, seed={args.seed}")
    results = {"iters": args.iters, "seed": args.seed, "models": {}}
    for model in MODELS:
        rows = data.get(model, {})
        n = len(rows)
        per_task = {}
        for task in TASKS:
            vals = [r[task] for r in rows.values() if r[task] is not None]
            point, lo, hi = bootstrap_ci(vals, args.iters, args.seed)
            per_task[task] = {
                "n": len(vals),
                "mean": point,
                "ci_low": lo,
                "ci_high": hi,
                "ci_half_width": round((hi - lo) / 2, 3) if hi is not None else None,
            }
        results["models"][model] = {
            "display": MODEL_DISPLAY[model],
            "n_articles": n,
            "tasks": per_task,
        }

    out_path = ROOT / "bootstrap_ci.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print()
    print("Bootstrap 95% CIs (overall_score):")
    print(f"  {'Model':<22} {'mean':>6} {'CI':>17}  {'half-width':>10}")
    for model in MODELS:
        t = results["models"][model]["tasks"]["overall_score"]
        print(f"  {MODEL_DISPLAY[model]:<22} {t['mean']:>6.2f} "
              f"  [{t['ci_low']:.2f}, {t['ci_high']:.2f}]   ±{t['ci_half_width']:.2f}")

    print()
    print("Pairwise non-overlap check (overall_score CIs):")
    for i, m1 in enumerate(MODELS):
        for m2 in MODELS[i+1:]:
            t1 = results["models"][m1]["tasks"]["overall_score"]
            t2 = results["models"][m2]["tasks"]["overall_score"]
            non_overlap = t1["ci_low"] > t2["ci_high"] or t2["ci_low"] > t1["ci_high"]
            sym = "OK separated" if non_overlap else "** overlapping"
            print(f"  {MODEL_DISPLAY[m1]:<18} vs {MODEL_DISPLAY[m2]:<18} {sym}")

    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
