"""Combine 5 categories of 100 samples each into a single 500-article dataset.

Sources:
  - Culture, Politics, Tech: from arabic_topic_dataset.json
  - Finance: from alwatan_finance_dataset.json
  - Sports: from sports_dataset.json
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

TOPIC_FILE = ROOT / "arabic_topic_dataset.json"
FINANCE_FILE = ROOT / "alwatan_finance_dataset.json"
SPORTS_FILE = ROOT / "sports_dataset.json"
OUT_FILE = ROOT / "arabic_500_dataset.json"

PER_CATEGORY = 100


def load(p: Path) -> list[dict]:
    return json.loads(p.read_text(encoding="utf-8"))


def normalize(article: dict, category: str, idx: int) -> dict:
    """Normalize an article record to a common shape."""
    body = (article.get("body") or "").strip()
    title = (article.get("title") or "").strip()
    if not title:
        first = re.split(r"[.\n]", body, maxsplit=1)[0].strip()
        title = first[:100] + ("..." if len(first) > 100 else "")
    return {
        "id": f"{category.upper()}_{idx:03d}",
        "title": title,
        "body": body,
        "source": category,
        "category": category,
        "word_count": article.get("word_count"),
        "date_published": article.get("date_published"),
    }


def main():
    topic_data = load(TOPIC_FILE)
    finance_data = load(FINANCE_FILE)
    sports_data = load(SPORTS_FILE)

    # Group topic data by source name
    by_topic: dict[str, list[dict]] = {}
    for s in topic_data:
        src = s.get("source", "").strip()
        by_topic.setdefault(src, []).append(s)

    print("Topic file contents:")
    for k, v in by_topic.items():
        print(f"  {k}: {len(v)}")

    unified = []

    def add_category(name: str, source_list: list[dict]):
        picked = source_list[:PER_CATEGORY]
        for i, art in enumerate(picked, start=1):
            unified.append(normalize(art, name, i))
        print(f"  {name}: {len(picked)} added")

    print("\nBuilding unified dataset:")
    add_category("culture", by_topic.get("Culture", []))
    add_category("politics", by_topic.get("Politics", []))
    add_category("tech", by_topic.get("Tech", []))
    add_category("finance", finance_data)
    add_category("sports", sports_data)

    OUT_FILE.write_text(
        json.dumps(unified, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\nTotal: {len(unified)} articles")
    print(f"Output: {OUT_FILE}")
    print(f"Size: {OUT_FILE.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
