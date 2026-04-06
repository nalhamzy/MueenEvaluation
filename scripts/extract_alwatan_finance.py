"""Extract 100 valid alwatan/finance samples from training_dataset_v2.csv."""

import csv
import json
import re
import sys
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "training_dataset_v2.csv"
OUT_PATH = Path(__file__).parent.parent / "alwatan_finance_dataset.json"

CATEGORY = "alwatan/finance"
TARGET = 100
MIN_WORDS = 100
MAX_WORDS = 1000


def count_words(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def is_valid_arabic(text: str) -> bool:
    return len(re.findall(r"[\u0600-\u06FF]", text)) >= 50


def extract_title(body: str) -> str:
    body = body.strip()
    first = re.split(r"[.\n]", body, maxsplit=1)[0].strip()
    return first[:100] + ("..." if len(first) > 100 else "")


def main():
    csv.field_size_limit(10_000_000)
    samples = []
    seen = 0
    skipped_words = 0
    skipped_arabic = 0

    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("source", "").strip() != CATEGORY:
                continue
            seen += 1
            body = (row.get("text") or "").strip()
            if not body:
                continue
            wc = count_words(body)
            if wc < MIN_WORDS or wc > MAX_WORDS:
                skipped_words += 1
                continue
            if not is_valid_arabic(body):
                skipped_arabic += 1
                continue

            samples.append({
                "id": f"FIN_{len(samples)+1:03d}",
                "title": extract_title(body),
                "body": body,
                "source": CATEGORY,
                "word_count": wc,
            })
            if len(samples) >= TARGET:
                break

    OUT_PATH.write_text(
        json.dumps(samples, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Scanned {seen} {CATEGORY} rows")
    print(f"Skipped (word count out of range): {skipped_words}")
    print(f"Skipped (insufficient Arabic): {skipped_arabic}")
    print(f"Selected: {len(samples)}")
    print(f"Output: {OUT_PATH}")


if __name__ == "__main__":
    main()
