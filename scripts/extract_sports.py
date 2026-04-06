"""Extract 100 valid sports samples from data/sport_articles.json."""

import json
import re
from pathlib import Path

SRC = Path(__file__).parent.parent / "data" / "sport_articles.json"
OUT = Path(__file__).parent.parent / "sports_dataset.json"

TARGET = 100
MIN_WORDS = 100
MAX_WORDS = 1000


def count_words(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def is_valid_arabic(text: str) -> bool:
    return len(re.findall(r"[\u0600-\u06FF]", text)) >= 50


def extract_title(article: dict) -> str:
    t = (article.get("title") or "").strip()
    if t:
        return t[:200]
    body = (article.get("body") or "").strip()
    first = re.split(r"[.\n]", body, maxsplit=1)[0].strip()
    return first[:100] + ("..." if len(first) > 100 else "")


def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print(f"ERROR: expected JSON array, got {type(data).__name__}")
        return

    print(f"Total records in source: {len(data)}")

    samples = []
    skipped_words = 0
    skipped_arabic = 0
    skipped_no_body = 0

    for art in data:
        body = (art.get("body") or "").strip()
        if not body:
            skipped_no_body += 1
            continue
        wc = count_words(body)
        if wc < MIN_WORDS or wc > MAX_WORDS:
            skipped_words += 1
            continue
        if not is_valid_arabic(body):
            skipped_arabic += 1
            continue

        samples.append({
            "id": f"SPORT_{len(samples)+1:03d}",
            "title": extract_title(art),
            "body": body,
            "source": "sports",
            "word_count": wc,
            "date_published": art.get("date_published") or art.get("date"),
        })
        if len(samples) >= TARGET:
            break

    OUT.write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Skipped (no body):     {skipped_no_body}")
    print(f"Skipped (word count):  {skipped_words}")
    print(f"Skipped (not Arabic):  {skipped_arabic}")
    print(f"Selected: {len(samples)}")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()
