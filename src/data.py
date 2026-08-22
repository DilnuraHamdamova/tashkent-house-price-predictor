"""Current-listing loading, cleaning, validation, and feature engineering."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import numpy as np
import pandas as pd

TARGET_COLUMN = "listing_price_usd"
RAW_INPUT_COLUMNS = (
    "district",
    "rooms",
    "size_m2",
    "level",
    "max_levels",
    "is_new_building",
)
NUMERIC_COLUMNS = (
    "rooms",
    "size_m2",
    "level",
    "max_levels",
    "is_new_building",
    "floor_ratio",
)
FEATURE_COLUMNS = ("district", *NUMERIC_COLUMNS)
FINGERPRINT_COLUMNS = RAW_INPUT_COLUMNS

# Conservative validity limits fixed before model evaluation. They remove obvious
# currency/category/unit errors while retaining rare high-end apartments.
VALID_RANGES = {
    "rooms": (1, 20),
    "size_m2": (15, 1000),
    "level": (1, 50),
    "max_levels": (1, 50),
    TARGET_COLUMN: (10_000, 5_000_000),
}


def _validate_features(features: pd.DataFrame) -> None:
    if features.empty:
        raise ValueError("Dataset is empty")
    if features[list(RAW_INPUT_COLUMNS)].isna().any().any():
        raise ValueError("Input features contain missing or non-numeric values")
    for column in ("rooms", "size_m2", "level", "max_levels"):
        if (features[column] <= 0).any():
            raise ValueError(f"{column} must be positive")
    if (features["level"] > features["max_levels"]).any():
        raise ValueError("Apartment level cannot exceed building max_levels")
    if not features["is_new_building"].isin([0, 1]).all():
        raise ValueError("is_new_building must be 0 or 1")


def prepare_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize and validate raw apartment fields, then add floor ratio."""
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


def _valid_listing_mask(frame: pd.DataFrame) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    for column, (minimum, maximum) in VALID_RANGES.items():
        numeric = pd.to_numeric(frame[column], errors="coerce")
        mask &= numeric.between(minimum, maximum)
    mask &= pd.to_numeric(frame["level"], errors="coerce") <= pd.to_numeric(
        frame["max_levels"], errors="coerce"
    )
    mask &= pd.to_numeric(frame["is_new_building"], errors="coerce").isin([0, 1])
    return mask


def load_dataset(path: str | Path) -> tuple[pd.DataFrame, pd.Series, dict[str, object]]:
    """Load a 2026 snapshot, reject invalid rows, and remove exact listing duplicates."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    raw = pd.read_csv(path)
    required = {*RAW_INPUT_COLUMNS, TARGET_COLUMN}
    missing = sorted(required.difference(raw.columns))
    if missing:
        raise ValueError(f"Dataset is missing columns: {', '.join(missing)}")

    source_rows = len(raw)
    missing_required_rows = int(raw[list(required)].isna().any(axis=1).sum())
    valid_mask = _valid_listing_mask(raw) & ~raw[list(required)].isna().any(axis=1)
    valid = raw.loc[valid_mask].copy()
    invalid_rows_removed = source_rows - len(valid)

    duplicate_subset = [*FINGERPRINT_COLUMNS, TARGET_COLUMN]
    duplicate_rows_removed = int(valid.duplicated(duplicate_subset).sum())
    clean = valid.drop_duplicates(duplicate_subset).reset_index(drop=True)

    features = prepare_features(clean)
    target = pd.to_numeric(clean[TARGET_COLUMN], errors="coerce")
    if target.isna().any() or not np.isfinite(target).all() or (target <= 0).any():
        raise ValueError("Listing price must contain only positive numeric values")

    feature_group_count = int(clean.groupby(list(FINGERPRINT_COLUMNS)).ngroups)
    audit: dict[str, object] = {
        "source_rows": source_rows,
        "missing_required_rows": missing_required_rows,
        "invalid_rows_removed": invalid_rows_removed,
        "duplicate_rows_removed": duplicate_rows_removed,
        "modeling_rows": len(clean),
        "property_feature_groups": feature_group_count,
        "district_count": int(features["district"].nunique()),
        "target_name": TARGET_COLUMN,
        "target_currency": "USD",
        "target_meaning": "advertised asking price, not completed sale price",
        "listing_date_min": str(clean["listing_date"].min()) if "listing_date" in clean else None,
        "listing_date_max": str(clean["listing_date"].max()) if "listing_date" in clean else None,
        "valid_ranges": VALID_RANGES,
    }
    return features, target.astype(float), audit


def make_features(row: Mapping[str, object]) -> pd.DataFrame:
    """Create one validated inference row from raw values."""
    return prepare_features(pd.DataFrame([row]))
