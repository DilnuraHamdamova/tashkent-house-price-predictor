"""Command-line model training entry point."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from .data import load_dataset
from .model import save_artifact, train_best_model

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the Tashkent apartment price predictor")
    parser.add_argument(
        "--data",
        type=Path,
        default=PROJECT_ROOT / "data" / "apartment_listings_2026.csv",
        help="CSV dataset path",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts" / "apartment_price_pipeline.joblib",
        help="Serialized model pipeline path",
    )
    parser.add_argument(
        "--metrics-output",
        type=Path,
        default=PROJECT_ROOT / "artifacts" / "metrics.json",
        help="JSON metrics path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    features, target, audit = load_dataset(args.data)
    model, metadata = train_best_model(features, target)
    metadata["data_audit"] = audit
    output = save_artifact(model, metadata, args.output)
    args.metrics_output.parent.mkdir(parents=True, exist_ok=True)
    args.metrics_output.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame.from_dict(metadata["experiments"], orient="index").rename_axis(
        "model"
    ).reset_index().to_csv(reports_dir / "model_comparison.csv", index=False)
    pd.DataFrame.from_dict(metadata["protected_test_comparison"], orient="index").rename_axis(
        "model"
    ).reset_index().to_csv(reports_dir / "protected_test_metrics.csv", index=False)
    pd.DataFrame(metadata["largest_test_errors"]).to_csv(
        reports_dir / "largest_errors.csv", index=False
    )
    pd.DataFrame.from_dict(metadata["district_test_metrics"], orient="index").rename_axis(
        "district"
    ).reset_index().to_csv(reports_dir / "district_metrics.csv", index=False)
    print(f"Saved {metadata['model_name']} pipeline to {output}")
    print(f"Saved evaluation metadata to {args.metrics_output}")
    print(json.dumps(metadata["protected_test_comparison"], indent=2))


if __name__ == "__main__":
    main()
