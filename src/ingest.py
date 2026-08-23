"""Source-neutral normalization for approved apartment listing exports."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

STANDARD_COLUMNS = (
    "source",
    "listing_id",
    "listing_date",
    "district",
    "rooms",
    "listing_price_usd",
    "source_url",
    "size_m2",
    "level",
    "max_levels",
    "is_new_building",
    "collected_at_utc",
)
REQUIRED_SOURCE_COLUMNS = tuple(column for column in STANDARD_COLUMNS if column != "source")


def normalize_export(path: str | Path, source: str | None = None) -> pd.DataFrame:
    """Normalize one licensed/approved CSV export to the product schema."""
    path = Path(path)
    frame = pd.read_csv(path)
    missing = sorted(set(REQUIRED_SOURCE_COLUMNS).difference(frame.columns))
    if missing:
        raise ValueError(f"{path.name} is missing columns: {', '.join(missing)}")
    if "source" not in frame:
        if not source:
            raise ValueError(f"{path.name} needs a source column or --source value")
        frame["source"] = source
    frame["source"] = frame["source"].astype("string").str.strip()
    if frame["source"].isna().any() or (frame["source"] == "").any():
        raise ValueError(f"{path.name} contains an empty source name")
    return frame.loc[:, STANDARD_COLUMNS].copy()


def merge_exports(exports: list[pd.DataFrame]) -> pd.DataFrame:
    """Merge snapshots and retain the latest observation per source listing."""
    if not exports:
        raise ValueError("At least one source export is required")
    merged = pd.concat(exports, ignore_index=True)
    merged["collected_at_utc"] = pd.to_datetime(
        merged["collected_at_utc"], errors="raise", utc=True
    )
    merged["listing_date"] = pd.to_datetime(merged["listing_date"], errors="raise").dt.date
    merged = (
        merged.sort_values("collected_at_utc")
        .drop_duplicates(["source", "listing_id"], keep="last")
        .sort_values(["listing_date", "source", "listing_id"])
        .reset_index(drop=True)
    )
    merged["listing_date"] = merged["listing_date"].astype(str)
    merged["collected_at_utc"] = merged["collected_at_utc"].map(lambda value: value.isoformat())
    return merged
