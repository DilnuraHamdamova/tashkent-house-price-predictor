# Dataset card — 2026 Tashkent apartment listings

## Source and snapshot

- Source: [HATA apartments for sale in Tashkent](https://hata.uz/en/listings/sale/flats/tashkent)
- Snapshot collected: 22 August 2026 (Asia/Samarkand)
- Listing dates represented: 4–21 August 2026
- Source terms: [HATA Terms of use](https://hata.uz/en/terms), last updated 1 May 2025
- Collection script: `scripts/collect_current_listings.py apartment`
- Repository snapshot: `data/apartment_listings_2026.csv`

HATA describes itself as a platform displaying current listings from owners, agencies, and
developers. Its public `robots.txt` allows catalog pages and disallows API routes, so the
collector reads only rate-limited public catalog pages. It retains factual property fields and
source URLs, while excluding seller names, phone numbers, descriptions, and images.

HATA does not publish this catalog under an open-data license. This privacy-minimized snapshot
is included for educational reproducibility; source rights remain with HATA and listing authors.
Written redistribution permission is still a recommended confirmation before wider reuse.

## Target

`listing_price_usd` is the **advertised asking price in USD**. It is not a verified transaction
price, appraisal, or evidence of the amount ultimately paid.

## Schema

| Column | Meaning | Use |
|---|---|---|
| `listing_id` | Source listing identifier | Deduplication/audit only |
| `listing_date` | Date shown on the catalog | Recency audit only |
| `district` | Tashkent district | Categorical feature |
| `rooms` | Advertised room count | Numeric feature |
| `size_m2` | Advertised apartment area | Numeric feature |
| `level` | Apartment floor | Numeric feature |
| `max_levels` | Building floor count | Numeric feature |
| `is_new_building` | 1 new build, 0 resale | Binary feature |
| `listing_price_usd` | Advertised asking price | Regression target |
| `source_url` | Public evidence route | Audit only |
| `collected_at_utc` | Snapshot timestamp | Reproducibility audit |

`floor_ratio = level / max_levels` is calculated at runtime. Price per square metre is excluded
because it directly contains the target and would cause leakage.

## Quality and preprocessing decisions

- Parsed unique complete-feature listings: 4,867
- Rows outside conservative validity rules: 257 removed
- Exact feature + target duplicate rows: 396 removed
- Modeling rows: 4,214
- Identical feature fingerprints: 3,840 groups
- Districts represented: 11; Yangihayot is absent

Validity rules were fixed before evaluation: rooms 1–20, area 15–1,000 m², apartment/building
floors 1–50 with `level <= max_levels`, binary building type, and asking price $10,000–$5,000,000.
They remove obvious rental/currency/category/unit errors while retaining rare luxury listings.

Rows with identical `district + rooms + size + floor + building floors + new-build status`
remain in the same holdout and cross-validation group. This conservative rule prevents identical
feature fingerprints from leaking between train and evaluation splits, though it cannot prove
that differently described or slightly edited records are not the same physical apartment.

## Limitations

- Asking prices may differ from completed sale prices.
- The snapshot is current for August 2026, not a permanently live market feed.
- User-entered listings can be stale, wrong, duplicated, or miscategorized.
- Exact addresses/coordinates are not modeled, limiting within-district location precision.
- Condition, renovation, construction year, legal status, amenities, and seller type are absent.
- District coverage is uneven and Yangihayot has no retained modeling rows.
- Location and price patterns may reproduce existing geographic inequality.
- Use requires human review and recent comparable listings; it is not suitable for lending,
  taxation, legal appraisal, or an autonomous financial decision.
