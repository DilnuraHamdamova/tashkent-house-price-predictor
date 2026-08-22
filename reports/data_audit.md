# 2026 data audit

## Snapshot identity

- Source: HATA public Tashkent apartment-sale catalog
- Collected: 22 August 2026 (Asia/Samarkand)
- Listing dates: 4–21 August 2026
- Parsed unique complete-feature rows: 4,867
- Direct seller identity/contact/image/description retained: none

## Schema and missingness

The collector requires district, rooms, size, apartment floor, building floors, building type,
listing date, USD asking price, listing ID, and source URL. It skipped 477 catalog cards that did
not expose every required model field. The resulting CSV has no missing required values.

## Validity rules

Rules were set before evaluation and implemented in `src/data.py`:

| Field | Accepted rule |
|---|---|
| Rooms | 1–20 |
| Area | 15–1,000 m² |
| Apartment floor | 1–50 |
| Building floors | 1–50 |
| Floor relationship | apartment floor ≤ building floors |
| Building type | 0 resale or 1 new build |
| Asking price | $10,000–$5,000,000 |

These rules remove 257 obvious rental/category/currency/unit errors. They intentionally retain
rare luxury apartments rather than deleting rows by an outcome-driven IQR threshold.

## Duplicate and leakage controls

- Exact feature + target duplicates removed: 396
- Rows used for modeling: 4,214
- Unique feature fingerprints: 3,840

The fingerprint is `district + rooms + size_m2 + level + max_levels + is_new_building`.
All rows with an identical fingerprint stay in the same protected holdout group and the same CV
fold. This prevents exact-feature leakage even when asking prices differ. It is conservative—it
may group different apartments with identical attributes—but it cannot detect every relisting
whose feature values were edited.

## Distribution and representation

| District | Modeling rows |
|---|---:|
| Yunusobod | 630 |
| Shayhontohur | 619 |
| Olmazor | 415 |
| Sergeli | 407 |
| Yakkasaroy | 404 |
| Uchtepa | 399 |
| Bektemir | 346 |
| Chilonzor | 327 |
| Yashnobod | 302 |
| Mirzo Ulugbek | 207 |
| Mirobod | 158 |

Yangihayot is absent, so any prediction there must be treated as out of distribution. The median
cleaned listing has 3 rooms, 68 m², and an asking price of $85,000. The retained target remains
right-skewed because expensive current listings are legitimate parts of the advertised market.

## Leakage risks considered

- Price per m² is excluded because it directly contains the target.
- Target price is not used to define feature groups or splits.
- Encoding/scaling is fit inside each CV pipeline.
- Protected test groups are not used for model selection.
- Source IDs, URLs, and listing dates are audit-only, not model features.

## Remaining limitations

HATA labels are advertiser-provided asking prices, not verified sales. Exact address, renovation,
condition, building year, legal status, amenities, and seller type are absent. Source permission
for broad redistribution is not explicitly granted. The snapshot is current for August 2026 but
will drift as the market changes.
