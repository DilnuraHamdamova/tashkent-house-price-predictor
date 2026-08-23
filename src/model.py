"""Leakage-safe model comparison, evaluation, persistence, and inference."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import StratifiedGroupKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import FEATURE_COLUMNS, NUMERIC_COLUMNS, make_features

RANDOM_STATE = 42
TEST_SIZE = 0.20


def _preprocessor(*, scale_numeric: bool) -> ColumnTransformer:
    numeric_transformer: str | StandardScaler = StandardScaler() if scale_numeric else "passthrough"
    return ColumnTransformer(
        [
            ("district", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["district"]),
            ("numeric", numeric_transformer, list(NUMERIC_COLUMNS)),
        ],
        remainder="drop",
    )


def candidate_models() -> dict[str, Any]:
    """Return one naive baseline and three meaningful regression approaches."""
    ridge = Pipeline([("prepare", _preprocessor(scale_numeric=True)), ("model", Ridge(alpha=10.0))])
    return {
        "median_baseline": Pipeline(
            [
                ("prepare", _preprocessor(scale_numeric=False)),
                ("model", DummyRegressor(strategy="median")),
            ]
        ),
        "log_ridge": TransformedTargetRegressor(
            regressor=ridge,
            func=np.log1p,
            inverse_func=np.expm1,
        ),
        "random_forest": Pipeline(
            [
                ("prepare", _preprocessor(scale_numeric=False)),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=250,
                        min_samples_leaf=2,
                        max_features=0.8,
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "gradient_boosting": Pipeline(
            [
                ("prepare", _preprocessor(scale_numeric=False)),
                (
                    "model",
                    GradientBoostingRegressor(
                        n_estimators=250,
                        learning_rate=0.04,
                        max_depth=2,
                        min_samples_leaf=4,
                        loss="huber",
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
    }


def regression_metrics(actual: pd.Series | np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    actual_array = np.asarray(actual, dtype=float)
    errors = actual_array - predicted
    return {
        "mae_usd": float(mean_absolute_error(actual_array, predicted)),
        "rmse_usd": float(np.sqrt(np.mean(errors**2))),
        "r2": float(r2_score(actual_array, predicted)),
        "mape_percent": float(mean_absolute_percentage_error(actual_array, predicted) * 100),
    }


def train_best_model(features: pd.DataFrame, target: pd.Series) -> tuple[Any, dict[str, Any]]:
    """Select by training-only CV, evaluate on test once, then refit all rows."""
    if len(features) < 100:
        raise ValueError("At least 100 rows are required for model training")

    feature_groups = pd.util.hash_pandas_object(features, index=False).astype(str)
    group_frame = pd.DataFrame(
        {"group": feature_groups, "district": features["district"].astype(str)}
    ).drop_duplicates("group")
    train_groups, test_groups = train_test_split(
        group_frame,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=group_frame["district"],
    )
    train_mask = feature_groups.isin(train_groups["group"])
    test_mask = feature_groups.isin(test_groups["group"])
    train_x, test_x = features.loc[train_mask], features.loc[test_mask]
    train_y, test_y = target.loc[train_mask], target.loc[test_mask]
    train_feature_groups = feature_groups.loc[train_mask]
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    splits = list(cv.split(train_x, train_x["district"], groups=train_feature_groups))
    holdout_group_overlap = len(set(train_groups["group"]) & set(test_groups["group"]))
    cv_group_overlap_max = max(
        len(
            set(train_feature_groups.iloc[fold_train])
            & set(train_feature_groups.iloc[fold_validation])
        )
        for fold_train, fold_validation in splits
    )
    if holdout_group_overlap or cv_group_overlap_max:
        raise RuntimeError("Feature groups overlap across an evaluation boundary")
    models = candidate_models()
    experiments: dict[str, dict[str, float]] = {}

    for name, model in models.items():
        scores = cross_validate(
            model,
            train_x,
            train_y,
            cv=splits,
            scoring=("neg_mean_absolute_error", "neg_root_mean_squared_error", "r2"),
            n_jobs=-1,
        )
        experiments[name] = {
            "cv_mae_mean_usd": float(-scores["test_neg_mean_absolute_error"].mean()),
            "cv_mae_std_usd": float(scores["test_neg_mean_absolute_error"].std()),
            "cv_rmse_mean_usd": float(-scores["test_neg_root_mean_squared_error"].mean()),
            "cv_r2_mean": float(scores["test_r2"].mean()),
            "fit_time_mean_seconds": float(scores["fit_time"].mean()),
        }

    selectable = [name for name in models if name != "median_baseline"]
    selected_name = min(selectable, key=lambda name: experiments[name]["cv_mae_mean_usd"])

    test_comparison: dict[str, dict[str, float]] = {}
    selected_model: Any | None = None
    selected_predictions: np.ndarray | None = None
    for name in ("median_baseline", selected_name):
        fitted = candidate_models()[name].fit(train_x, train_y)
        predictions = np.asarray(fitted.predict(test_x), dtype=float)
        test_comparison[name] = regression_metrics(test_y, predictions)
        if name == selected_name:
            selected_model = fitted
            selected_predictions = predictions

    assert selected_model is not None and selected_predictions is not None
    error_frame = test_x.copy()
    error_frame["actual_usd"] = test_y
    error_frame["predicted_usd"] = selected_predictions
    error_frame["absolute_error_usd"] = np.abs(test_y.to_numpy() - selected_predictions)
    absolute_error_quantiles = {
        f"p{int(quantile * 100)}_usd": float(error_frame["absolute_error_usd"].quantile(quantile))
        for quantile in (0.5, 0.8, 0.9)
    }
    largest_errors = (
        error_frame.nlargest(10, "absolute_error_usd")
        .reset_index(names="source_index")
        .to_dict(orient="records")
    )

    district_metrics: dict[str, dict[str, float | int]] = {}
    for district, group in error_frame.groupby("district", observed=True):
        district_metrics[str(district)] = {
            "rows": int(len(group)),
            **regression_metrics(group["actual_usd"], group["predicted_usd"].to_numpy()),
        }

    final_model = candidate_models()[selected_name].fit(features, target)
    metadata: dict[str, Any] = {
        "model_name": selected_name,
        "trained_at_utc": datetime.now(timezone.utc).isoformat(),
        "random_state": RANDOM_STATE,
        "row_count": int(len(features)),
        "train_row_count": int(len(train_x)),
        "test_row_count": int(len(test_x)),
        "train_group_count": int(len(train_groups)),
        "test_group_count": int(len(test_groups)),
        "holdout_group_overlap": holdout_group_overlap,
        "cv_group_overlap_max": cv_group_overlap_max,
        "feature_columns": list(FEATURE_COLUMNS),
        "target": "listing_price_usd",
        "selection_rule": (
            "lowest 5-fold district-stratified, feature-group-safe CV MAE "
            "on the 80% development groups"
        ),
        "split_rule": (
            "identical apartment feature fingerprints stay in one split for holdout and CV"
        ),
        "experiments": experiments,
        "protected_test_comparison": test_comparison,
        "district_test_metrics": district_metrics,
        "largest_test_errors": largest_errors,
        "protected_test_absolute_error_quantiles": absolute_error_quantiles,
        "final_fit": "selected pipeline refitted on all de-duplicated rows after test evaluation",
        "training_ranges": {
            column: {"min": float(features[column].min()), "max": float(features[column].max())}
            for column in NUMERIC_COLUMNS
        },
        "known_districts": sorted(features["district"].astype(str).unique().tolist()),
    }
    return final_model, metadata


def save_artifact(model: Any, metadata: dict[str, Any], path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "metadata": metadata}, path, compress=3)
    return path


def load_artifact(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Model artifact not found: {path}. Run the training command first."
        )
    artifact = joblib.load(path)
    if not isinstance(artifact, dict) or not {"model", "metadata"}.issubset(artifact):
        raise ValueError(f"Invalid model artifact: {path}")
    return artifact


def predict_price(artifact: dict[str, Any], **raw_values: object) -> tuple[float, list[str]]:
    """Validate one apartment and return its predicted USD price plus OOD warnings."""
    features = make_features(raw_values)
    metadata = artifact["metadata"]
    warnings: list[str] = []
    district = str(features.iloc[0]["district"])
    if district not in metadata.get("known_districts", []):
        warnings.append(f"District '{district}' was not present in training data")
    for column, bounds in metadata.get("training_ranges", {}).items():
        value = float(features.iloc[0][column])
        if value < bounds["min"] or value > bounds["max"]:
            minimum = bounds["min"]
            maximum = bounds["max"]
            warnings.append(
                f"{column}={value:g} is outside training range [{minimum:g}, {maximum:g}]"
            )
    prediction = float(max(artifact["model"].predict(features)[0], 0.0))
    return prediction, warnings
