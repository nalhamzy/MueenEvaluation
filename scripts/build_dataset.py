"""Build a topic-balanced Arabic news dataset from raw text files.

Reads from data/<Topic>/*.txt and selects 100 valid samples per topic.
Validity: 100-1000 words, non-empty.
Outputs a JSON file with 100 samples per topic, each as an article record.
"""

import os
import re
import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = Path(__file__).parent.parent / "arabic_topic_dataset.json"

MIN_WORDS = 100
MAX_WORDS = 1000
SAMPLES_PER_TOPIC = 100


def count_words(text: str) -> int:
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def extract_title(body: str) -> str:
    """Use the first sentence (or first 80 chars) as the title."""
    body = body.strip()
    # Try to split on Arabic period or first newline
    first_sent = re.split(r"[.\n]", body, maxsplit=1)[0].strip()
    if len(first_sent) > 100:
        first_sent = first_sent[:100].rstrip() + "..."
    return first_sent


def is_valid_arabic(text: str) -> bool:
    """Check that the text contains a meaningful amount of Arabic characters."""
    arabic_chars = len(re.findall(r"[\u0600-\u06FF]", text))
    return arabic_chars >= 50


def process_topic(topic_dir: Path, target: int) -> list[dict]:
    """Process a topic folder and return up to `target` valid samples."""
    samples = []
    files = sorted(topic_dir.glob("*.txt"))

    if not files:
        print(f"  [SKIP] {topic_dir.name}: no .txt files")
        return []

    print(f"  [{topic_dir.name}] scanning {len(files)} files...")

    for f in files:
        if len(samples) >= target:
            break
        try:
            body = f.read_text(encoding="utf-8").strip()
        except (UnicodeDecodeError, OSError):
            try:
                body = f.read_text(encoding="cp1256").strip()
            except Exception:
                continue

        if not body:
            continue

        wc = count_words(body)
        if wc < MIN_WORDS or wc > MAX_WORDS:
            continue

        if not is_valid_arabic(body):
            continue

        samples.append({
            "id": f"{topic_dir.name}_{f.stem}",
            "title": extract_title(body),
            "body": body,
            "source": topic_dir.name,
            "word_count": wc,
        })

    print(f"  [{topic_dir.name}] selected {len(samples)} valid samples")
    return samples


def main():
    if not DATA_DIR.exists():
        print(f"ERROR: data directory not found at {DATA_DIR}", file=sys.stderr)
        sys.exit(1)

    all_samples = []
    topic_summary = {}

    for topic_dir in sorted(DATA_DIR.iterdir()):
        if not topic_dir.is_dir():
            continue
        samples = process_topic(topic_dir, SAMPLES_PER_TOPIC)
        all_samples.extend(samples)
        topic_summary[topic_dir.name] = len(samples)

    # Re-id sequentially with topic prefix
    seq = 1
    for s in all_samples:
        s["seq_id"] = seq
        seq += 1

    OUTPUT_FILE.write_text(
        json.dumps(all_samples, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print("=" * 50)
    print("DATASET BUILD COMPLETE")
    print("=" * 50)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Total samples: {len(all_samples)}")
    print("By topic:")
    for topic, count in sorted(topic_summary.items()):
        marker = "OK" if count == SAMPLES_PER_TOPIC else f"({count}/{SAMPLES_PER_TOPIC})"
        print(f"  {topic:<15} {count:>4} samples {marker}")


if __name__ == "__main__":
    main()
