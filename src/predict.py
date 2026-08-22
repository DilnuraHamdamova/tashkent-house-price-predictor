"""Command-line prediction entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from .model import load_artifact, predict_price

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict a Tashkent apartment listing price")
    parser.add_argument("--district", required=True, help="Tashkent district name")
    parser.add_argument("--size", type=float, required=True, help="Apartment size in square metres")
    parser.add_argument("--rooms", type=int, required=True, help="Number of rooms")
    parser.add_argument("--level", type=int, required=True, help="Apartment floor")
    parser.add_argument("--max-levels", type=int, required=True, help="Building floor count")
    parser.add_argument(
        "--new-building",
        action="store_true",
        help="Mark the listing as a new-build apartment",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=PROJECT_ROOT / "artifacts" / "house_price_pipeline.joblib",
        help="Trained model pipeline path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    artifact = load_artifact(args.model)
    price, warnings = predict_price(
        artifact,
        district=args.district,
        size_m2=args.size,
        rooms=args.rooms,
        level=args.level,
        max_levels=args.max_levels,
        is_new_building=int(args.new_building),
    )
    print(f"Estimated listing price: ${price:,.0f} USD")
    for warning in warnings:
        print(f"Warning: {warning}")


if __name__ == "__main__":
    main()
