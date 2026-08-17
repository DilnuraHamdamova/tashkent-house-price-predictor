"""Dataset loading, cleaning, validation, and feature engineering."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import numpy as np
import pandas as pd

TARGET_COLUMN = "price"
RAW_INPUT_COLUMNS = ("district", "rooms", "size", "level", "max_levels", "lat", "lng")
NUMERIC_COLUMNS = ("rooms", "size", "level", "max_levels", "lat", "lng", "floor_ratio")
FEATURE_COLUMNS = ("district", *NUMERIC_COLUMNS)


def _validate_features(features: pd.DataFrame) -> None:
    if features.empty:
        raise ValueError("Dataset is empty")
    if features[list(RAW_INPUT_COLUMNS)].isna().any().any():
        raise ValueError("Input features contain missing or non-numeric values")
    positive = ("rooms", "size", "level", "max_levels")
    if (features[list(positive)] <= 0).any().any():
        raise ValueError("Rooms, size, level, and max_levels must be positive")
    if (features["level"] > features["max_levels"]).any():
        raise ValueError("Apartment level cannot exceed building max_levels")
    if not features["lat"].between(-90, 90).all() or not features["lng"].between(-180, 180).all():
        raise ValueError("Latitude or longitude is outside the valid geographic range")


def prepare_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize and validate raw apartment fields, then add floor_ratio."""
    missing = [column for column in RAW_INPUT_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    features = frame.loc[:, RAW_INPUT_COLUMNS].copy()
    features["district"] = features["district"].astype("string").str.strip()
    if features["district"].isna().any() or (features["district"] == "").any():
        raise ValueError("District must be a non-empty string")
    for column in RAW_INPUT_COLUMNS[1:]:
        features[column] = pd.to_numeric(features[column], errors="coerce")
    _validate_features(features)
    features["floor_ratio"] = features["level"] / features["max_levels"]
    return features.loc[:, FEATURE_COLUMNS]


def load_dataset(path: str | Path) -> tuple[pd.DataFrame, pd.Series, dict[str, object]]:
    """Load CSV, remove exact duplicate listings, and return features, target, audit."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    raw = pd.read_csv(path)
    required = {*RAW_INPUT_COLUMNS, TARGET_COLUMN}
    missing = sorted(required.difference(raw.columns))
    if missing:
        raise ValueError(f"Dataset is missing columns: {', '.join(missing)}")
    original_rows = len(raw)
    duplicate_rows = int(raw.duplicated().sum())
    clean = raw.drop_duplicates().reset_index(drop=True)
    features = prepare_features(clean)
    target = pd.to_numeric(clean[TARGET_COLUMN], errors="coerce")
    if target.isna().any() or not np.isfinite(target).all() or (target <= 0).any():
        raise ValueError("Price must contain only positive numeric values")
    audit: dict[str, object] = {
        "source_rows": original_rows,
        "duplicate_rows_removed": duplicate_rows,
        "training_rows": len(clean),
        "missing_values": int(clean[list(required)].isna().sum().sum()),
        "district_count": int(features["district"].nunique()),
        "target_currency": "USD",
    }
    return features, target.astype(float), audit


def make_features(row: Mapping[str, object]) -> pd.DataFrame:
    """Create one validated inference row from raw values."""
    return prepare_features(pd.DataFrame([row]))
