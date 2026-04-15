"""Tests for the deterministic article sampling script."""

import sys
import os
from pathlib import Path

# Add scripts dir to path so we can import sample_100
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))

import sample_100
from sample_100 import sample_articles, CATEGORIES


def test_sample_100_picks_20_per_category():
    """Should return 100 articles total, 20 from each of 5 categories."""
    samples = sample_articles(seed=42, per_category=20)
    assert len(samples) == 100

    by_cat: dict[str, int] = {}
    for s in samples:
        cat = (s.get("category") or s.get("source") or "").lower()
        by_cat[cat] = by_cat.get(cat, 0) + 1

    for cat in CATEGORIES:
        assert by_cat.get(cat) == 20, f"Expected 20 {cat}, got {by_cat.get(cat)}"


def test_sample_100_is_deterministic():
    """Same seed → identical selection across multiple calls."""
    s1 = sample_articles(seed=42, per_category=20)
    s2 = sample_articles(seed=42, per_category=20)
    assert [a["id"] for a in s1] == [a["id"] for a in s2]


def test_sample_100_different_seeds_differ():
    """Different seeds should produce different selections."""
    s1 = sample_articles(seed=42, per_category=20)
    s2 = sample_articles(seed=99, per_category=20)
    # At least some IDs should differ
    ids1 = {a["id"] for a in s1}
    ids2 = {a["id"] for a in s2}
    assert ids1 != ids2


def test_sample_smaller_per_category():
    """Should support smaller samples (e.g. 5 per cat = 25 total) for smoke tests."""
    samples = sample_articles(seed=42, per_category=5)
    assert len(samples) == 25
