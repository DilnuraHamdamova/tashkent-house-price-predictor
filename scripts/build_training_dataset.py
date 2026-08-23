"""Merge approved source exports into one versioned training CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.ingest import merge_exports, normalize_export


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="Approved source CSV exports")
    parser.add_argument(
        "--source", help="Source name for single-source files without source column"
    )
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.source and len(args.inputs) != 1:
        raise ValueError("--source can only be used with one input; otherwise add source columns")
    exports = [normalize_export(path, args.source) for path in args.inputs]
    merged = merge_exports(exports)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(args.output, index=False)
    print(
        f"Saved {len(merged):,} latest source listings from "
        f"{merged['source'].nunique()} source(s) to {args.output}"
    )


if __name__ == "__main__":
    main()
