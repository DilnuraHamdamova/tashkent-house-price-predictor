from __future__ import annotations

import json
from pathlib import Path

from src.data import load_dataset

ROOT = Path(__file__).resolve().parents[1]


def test_committed_2026_snapshot_audit() -> None:
    features, target, audit = load_dataset(ROOT / "data" / "apartment_listings_2026.csv")

    assert len(features) == len(target) == 4_214
    assert audit["source_rows"] == 4_867
    assert audit["invalid_rows_removed"] == 257
    assert audit["duplicate_rows_removed"] == 396
    assert audit["property_feature_groups"] == 3_840
    assert audit["listing_date_min"] == "2026-08-04"
    assert audit["listing_date_max"] == "2026-08-21"


def test_committed_metrics_are_group_safe_and_current() -> None:
    metrics = json.loads((ROOT / "artifacts" / "metrics.json").read_text(encoding="utf-8"))

    assert metrics["target"] == "listing_price_usd"
    assert metrics["holdout_group_overlap"] == 0
    assert metrics["cv_group_overlap_max"] == 0
    assert metrics["data_audit"]["listing_date_max"].startswith("2026-")
