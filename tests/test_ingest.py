from __future__ import annotations

import pandas as pd
import pytest

from src.ingest import merge_exports, normalize_export


def source_row(**updates):
    row = {
        "listing_id": 10,
        "listing_date": "2026-08-20",
        "district": "Chilonzor",
        "rooms": 3,
        "listing_price_usd": 70_000,
        "source_url": "https://example.test/10",
        "size_m2": 70,
        "level": 3,
        "max_levels": 5,
        "is_new_building": 0,
        "collected_at_utc": "2026-08-20T12:00:00+00:00",
    }
    return {**row, **updates}


def test_normalize_export_adds_explicit_source(tmp_path):
    path = tmp_path / "export.csv"
    pd.DataFrame([source_row()]).to_csv(path, index=False)
    result = normalize_export(path, source="approved-partner")
    assert result.iloc[0]["source"] == "approved-partner"


def test_merge_exports_keeps_latest_source_listing():
    earlier = pd.DataFrame([{**source_row(), "source": "partner"}])
    later = pd.DataFrame(
        [
            {
                **source_row(
                    listing_price_usd=75_000,
                    collected_at_utc="2026-08-21T12:00:00+00:00",
                ),
                "source": "partner",
            }
        ]
    )
    result = merge_exports([earlier, later])
    assert len(result) == 1
    assert result.iloc[0]["listing_price_usd"] == 75_000


def test_normalize_export_rejects_unknown_provenance(tmp_path):
    path = tmp_path / "export.csv"
    pd.DataFrame([source_row()]).to_csv(path, index=False)
    with pytest.raises(ValueError, match="source column"):
        normalize_export(path)
