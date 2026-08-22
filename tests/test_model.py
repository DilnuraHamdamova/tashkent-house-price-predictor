from __future__ import annotations

import numpy as np
import pandas as pd

from src.data import prepare_features
from src.model import (
    candidate_models,
    load_artifact,
    predict_price,
    save_artifact,
    train_best_model,
)


def synthetic_dataset(rows: int = 120) -> tuple[pd.DataFrame, pd.Series]:
    rng = np.random.default_rng(42)
    raw = pd.DataFrame(
        {
            "district": np.where(np.arange(rows) % 2, "Chilonzor", "Yunusobod"),
            "rooms": rng.integers(1, 6, rows),
            "size_m2": rng.uniform(25, 180, rows),
            "level": rng.integers(1, 5, rows),
            "max_levels": np.full(rows, 5),
            "is_new_building": rng.integers(0, 2, rows),
        }
    )
    target = pd.Series(
        10_000
        + raw["size_m2"] * 700
        + raw["rooms"] * 2_500
        + (raw["district"] == "Yunusobod") * 8_000,
        dtype=float,
    )
    return prepare_features(raw), target


def test_experiment_set_contains_baseline_and_three_models() -> None:
    assert set(candidate_models()) == {
        "median_baseline",
        "log_ridge",
        "random_forest",
        "gradient_boosting",
    }


def test_train_save_load_and_predict(tmp_path) -> None:
    features, target = synthetic_dataset()
    model, metadata = train_best_model(features, target)
    path = save_artifact(model, metadata, tmp_path / "model.joblib")
    artifact = load_artifact(path)

    price, warnings = predict_price(
        artifact,
        district="Chilonzor",
        rooms=3,
        size_m2=70,
        level=3,
        max_levels=5,
        is_new_building=0,
    )

    assert price > 0
    assert warnings == []
    assert metadata["model_name"] != "median_baseline"
    assert "protected_test_comparison" in metadata
    assert metadata["holdout_group_overlap"] == 0
    assert metadata["cv_group_overlap_max"] == 0


def test_predict_warns_for_unseen_district(tmp_path) -> None:
    features, target = synthetic_dataset()
    model, metadata = train_best_model(features, target)
    artifact = {"model": model, "metadata": metadata}
    price, warnings = predict_price(
        artifact,
        district="Unknown",
        rooms=3,
        size_m2=70,
        level=3,
        max_levels=5,
        is_new_building=0,
    )
    assert price > 0
    assert any("not present" in warning for warning in warnings)
