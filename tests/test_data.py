from __future__ import annotations

import pandas as pd
import pytest

from src.data import FEATURE_COLUMNS, load_dataset, make_features

VALID_ROW = {
    "district": "Chilonzor",
    "rooms": 3,
    "size_m2": 70,
    "level": 3,
    "max_levels": 5,
    "is_new_building": 0,
}


def test_make_features_adds_floor_ratio() -> None:
    features = make_features(VALID_ROW)
    assert tuple(features.columns) == FEATURE_COLUMNS
    assert features.iloc[0]["floor_ratio"] == pytest.approx(0.6)


def test_make_features_rejects_invalid_floor() -> None:
    with pytest.raises(ValueError, match="cannot exceed"):
        make_features({**VALID_ROW, "level": 6})


def test_load_dataset_removes_exact_duplicates(tmp_path) -> None:
    row = {
        "listing_date": "2026-08-20",
        **VALID_ROW,
        "listing_price_usd": 60_000,
    }
    path = tmp_path / "data.csv"
    pd.DataFrame([row, row]).to_csv(path, index=False)

    features, target, audit = load_dataset(path)

    assert len(features) == len(target) == 1
    assert audit["duplicate_rows_removed"] == 1
    assert audit["target_currency"] == "USD"
    assert audit["target_meaning"] == "advertised asking price, not completed sale price"
