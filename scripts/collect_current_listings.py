"""Collect privacy-minimized 2026 Tashkent property listing snapshots.

Only public HATA catalog pages allowed by robots.txt are read. The snapshots retain
factual model inputs, listing date, price, and source URL. Seller names, contacts,
descriptions, and images are deliberately excluded.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = (
    "TashkentPropertyPriceCapstone/2.0 educational-research "
    "(privacy-minimized factual listing snapshot; contact via repository)"
)

CATALOGS = {
    "apartment": {
        "base_url": "https://hata.uz/en/listings/sale/flats/tashkent",
        "default_pages": 185,
        "default_output": PROJECT_ROOT / "data" / "apartment_listings_2026.csv",
    },
    "house": {
        "base_url": "https://hata.uz/en/listings/sale/houses/tashkent",
        "default_pages": 416,
        "default_output": PROJECT_ROOT / "data" / "house_listings_2026.csv",
    },
}

DISTRICT_NAMES = {
    "Almazar": "Olmazor",
    "Bektemir": "Bektemir",
    "Chilanzar": "Chilonzor",
    "Mirabad": "Mirobod",
    "Mirzo Ulugbek": "Mirzo Ulugbek",
    "Sergeli": "Sergeli",
    "Shaykhantakhur": "Shayhontohur",
    "Uchtepa": "Uchtepa",
    "Yakkasaray": "Yakkasaroy",
    "Yangihayot": "Yangihayot",
    "Yashnabad": "Yashnobod",
    "Yunusabad": "Yunusobod",
}
DISTRICT_PATTERN = "|".join(re.escape(name) for name in DISTRICT_NAMES)


def _plain_text(fragment: str) -> str:
    without_comments = re.sub(r"<!--.*?-->", "", fragment, flags=re.DOTALL)
    without_tags = re.sub(r"<[^>]+>", " ", without_comments)
    return " ".join(html.unescape(without_tags).replace("\xa0", " ").split())


def _match(pattern: str, text: str, field: str) -> str:
    result = re.search(pattern, text, flags=re.DOTALL)
    if result is None:
        raise ValueError(f"Could not parse {field}")
    return html.unescape(result.group(1))


def _common_fields(card: str, expected_action: str) -> dict[str, object]:
    card_text = _plain_text(card)
    if expected_action not in card_text:
        raise ValueError("Card is outside the requested catalog")
    relative_url = _match(r'href="(/en/listings/object/[^"]+)"', card, "URL")
    listing_id = int(_match(r"-(\d+)$", relative_url, "listing id"))
    label = _match(r'aria-label="([^"]*?-room apartment, [^"]*?m² for sale)"', card, "label")
    label_match = re.search(r"(\d+)-room apartment, ([\d.]+) m² for sale", label)
    if label_match is None:
        raise ValueError("Could not parse rooms and area")
    district_source = _match(rf"({DISTRICT_PATTERN}) District, Tashkent</span>", card, "district")
    date_text = _match(r'<div class="mt-2[^>]*>.*?<span>([^<>]+)</span>', card, "listing date")
    price_fragment = _match(r'<span class="font-extrabold[^>]*>(.*?)</span>', card, "price")
    price_digits = re.sub(r"[^0-9]", "", _plain_text(price_fragment))
    if not price_digits:
        raise ValueError("Could not parse price")
    return {
        "listing_id": listing_id,
        "listing_date": datetime.strptime(date_text, "%B %d, %Y").date().isoformat(),
        "district": DISTRICT_NAMES[district_source],
        "rooms": int(label_match.group(1)),
        "raw_area_m2": float(label_match.group(2)),
        "listing_price_usd": int(price_digits),
        "source_url": f"https://hata.uz{relative_url}",
    }


def parse_catalog_page(page_html: str, property_type: str) -> tuple[list[dict[str, object]], int]:
    """Parse model fields from one server-rendered catalog page."""
    rows: list[dict[str, object]] = []
    skipped = 0
    cards = re.findall(r"<article\b.*?</article>", page_html, flags=re.DOTALL)
    expected = "Sale" if property_type == "apartment" else "Sale Houses, dachas, cottages"
    for card in cards:
        try:
            common = _common_fields(card, expected)
            raw_area = float(common.pop("raw_area_m2"))
            if property_type == "apartment":
                floor_fragment = _match(r"(<span[^>]*>\d+/\d+.*?fl\.</span>)", card, "floor")
                floor_match = re.search(r"(\d+)\s*/\s*(\d+)\s*fl\.", _plain_text(floor_fragment))
                if floor_match is None:
                    raise ValueError("Could not parse floor")
                rows.append(
                    {
                        **common,
                        "size_m2": raw_area,
                        "level": int(floor_match.group(1)),
                        "max_levels": int(floor_match.group(2)),
                        "is_new_building": int("Sale New builds" in _plain_text(card)),
                    }
                )
            else:
                # Some advertisers enter sotix in a field labelled m². Values below
                # 20 cannot plausibly represent a complete house/plot and are converted.
                rows.append(
                    {
                        **common,
                        "area_m2": raw_area * 100 if raw_area < 20 else raw_area,
                        "raw_area_m2": raw_area,
                        "area_unit_corrected": int(raw_area < 20),
                    }
                )
        except ValueError:
            skipped += 1
    return rows, skipped


def fetch_page(base_url: str, page: int, retries: int = 3) -> str:
    url = base_url if page == 1 else f"{base_url}?page={page}"
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en"})
    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed HTTPS origins
                return response.read().decode("utf-8")
        except (HTTPError, URLError, TimeoutError) as error:
            if attempt == retries:
                raise RuntimeError(f"Failed to fetch {url}: {error}") from error
            time.sleep(attempt * 2)
    raise AssertionError("unreachable")


def write_snapshot(
    rows: list[dict[str, object]], output: Path, collected_at: str, *, partial: bool = False
) -> None:
    if not rows:
        raise ValueError("No listings were collected")
    output.parent.mkdir(parents=True, exist_ok=True)
    destination = output.with_suffix(".partial.csv") if partial else output
    fieldnames = list(rows[0]) + ["collected_at_utc"]
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(rows, key=lambda item: int(item["listing_id"])):
            writer.writerow({**row, "collected_at_utc": collected_at})


def collect(
    property_type: str, first_page: int, last_page: int, delay: float, output: Path
) -> list[dict[str, object]]:
    base_url = str(CATALOGS[property_type]["base_url"])
    collected_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    collected: dict[int, dict[str, object]] = {}
    skipped_total = 0
    for page in range(first_page, last_page + 1):
        page_rows, skipped = parse_catalog_page(fetch_page(base_url, page), property_type)
        skipped_total += skipped
        for row in page_rows:
            collected[int(row["listing_id"])] = row
        if page % 10 == 0:
            write_snapshot(list(collected.values()), output, collected_at, partial=True)
        print(
            f"{property_type} page {page}/{last_page}: {len(page_rows)} parsed, "
            f"{len(collected)} unique, {skipped_total} skipped total",
            flush=True,
        )
        if page < last_page:
            time.sleep(delay)
    rows = list(collected.values())
    write_snapshot(rows, output, collected_at)
    partial_path = output.with_suffix(".partial.csv")
    if partial_path.exists():
        partial_path.unlink()
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("property_type", choices=sorted(CATALOGS))
    parser.add_argument("--first-page", type=int, default=1)
    parser.add_argument("--last-page", type=int)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    catalog = CATALOGS[args.property_type]
    last_page = args.last_page or int(catalog["default_pages"])
    output = args.output or Path(catalog["default_output"])
    if args.first_page < 1 or last_page < args.first_page:
        raise ValueError("Page range is invalid")
    rows = collect(args.property_type, args.first_page, last_page, max(args.delay, 0.0), output)
    print(f"Saved {len(rows)} {args.property_type} listings to {output}")


if __name__ == "__main__":
    main()
