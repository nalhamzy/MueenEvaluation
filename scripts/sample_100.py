"""Deterministic sampler: pick N articles per category from arabic_500_dataset.json.

Usage:
    py scripts/sample_100.py [--seed 42] [--per-category 20]

Outputs:
    selected_100.json — array of selected articles (audit trail)
    Also exposes sample_articles() as importable function for tests.
"""

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATASET_FILE = ROOT / "arabic_500_dataset.json"
OUTPUT_FILE = ROOT / "selected_100.json"

CATEGORIES = ["culture", "politics", "tech", "finance", "sports"]


def load_dataset(path: Path = DATASET_FILE) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def sample_articles(seed: int = 42, per_category: int = 20,
                    dataset_path: Path | None = None) -> list[dict]:
    """Pick `per_category` articles from each category deterministically.

    Returns a list of dicts in category order (culture, politics, tech, finance, sports).
    Same seed always returns the same selection.
    """
    data = load_dataset(dataset_path or DATASET_FILE)

    by_category: dict[str, list[dict]] = defaultdict(list)
    for art in data:
        cat = (art.get("category") or art.get("source") or "").lower()
        if cat in CATEGORIES:
            by_category[cat].append(art)

    rng = random.Random(seed)
    selected = []
    for cat in CATEGORIES:
        pool = by_category.get(cat, [])
        if len(pool) < per_category:
            raise ValueError(
                f"Category '{cat}' has only {len(pool)} articles, need {per_category}"
            )
        # Sort pool by id for stable input order before sampling
        pool_sorted = sorted(pool, key=lambda a: a.get("id", ""))
        picks = rng.sample(pool_sorted, per_category)
        selected.extend(picks)

    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--per-category", type=int, default=20)
    args = parser.parse_args()

    samples = sample_articles(seed=args.seed, per_category=args.per_category)

    OUTPUT_FILE.write_text(
        json.dumps(samples, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    by_cat: dict[str, int] = defaultdict(int)
    for s in samples:
        by_cat[s.get("category", "?")] += 1

    print(f"Sampled {len(samples)} articles (seed={args.seed}):")
    for cat, n in sorted(by_cat.items()):
        print(f"  {cat:<10} {n}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
