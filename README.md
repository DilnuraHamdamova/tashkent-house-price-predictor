# Tashkent Apartment Listing Price Predictor

[![CI](https://github.com/DilnuraHamdamova/tashkent-house-price-predictor/actions/workflows/ci.yml/badge.svg)](https://github.com/DilnuraHamdamova/tashkent-house-price-predictor/actions/workflows/ci.yml)
[![Open demo in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DilnuraHamdamova/tashkent-house-price-predictor/blob/main/demo.ipynb)

**[View presentation](presentation/README.md)** · **[PowerPoint](presentation/Tashkent_House_Price_Defense.pptx)** · **[PDF](presentation/Tashkent_House_Price_Defense.pdf)**

**[Bugungi pitch uchun to‘liq o‘zbekcha qo‘llanma va exact English speech](docs/defense_day_guide_uz.md)**

An end-to-end regression capstone that estimates the advertised USD asking price of a Tashkent
apartment from current August 2026 listing attributes. The repository includes a reproducible
privacy-minimized snapshot, feature-group-safe evaluation, a saved inference pipeline, validation,
tests, a Colab demo, and defense evidence.

**Selected track:** Individual Project Track
**Student:** Dilnura Hamdamova

## Problem and scope

Buyers, sellers, agents, and market analysts need a quick reference estimate when comparing
current Tashkent apartment advertisements. This is supervised regression:

- **Input:** district, size (m²), rooms, apartment floor, building floors, new-build/resale.
- **Output:** estimated **2026 advertised asking price in USD**.
- **Primary metric:** MAE, because dollar error is directly understandable.
- **Supporting metrics:** RMSE, R², and MAPE.
- **Success criterion:** reduce baseline test MAE by at least 30%, reach test R² ≥ 0.60, and
  test MAPE ≤ 25%.
- **Non-goals:** completed sale-price verification, legal appraisal, price guarantee, lending,
  taxation, or autonomous financial decision-making.

## Current 2026 data

The committed `data/apartment_listings_2026.csv` is a privacy-minimized snapshot of public
[HATA Tashkent sale listings](https://hata.uz/en/listings/sale/flats/tashkent), collected on
22 August 2026. Listing dates range from 4–21 August 2026. The collector retains factual property
fields and source URLs but excludes seller identity, contacts, descriptions, and images.

The snapshot contains 4,867 unique complete-feature listings. Conservative range checks remove
257 obvious category/currency/unit errors, then 396 exact feature + target duplicates are removed,
leaving 4,214 modeling rows and 3,840 apartment-feature groups. Eleven districts are represented;
Yangihayot is absent. See [data/README.md](data/README.md) and
[reports/data_audit.md](reports/data_audit.md).

The target is an **advertised asking price**, not a verified transaction price. HATA does not
publish an open-data license; source rights remain with HATA and listing authors. Written
redistribution permission is a recommended external confirmation before wider reuse.

## Method

The holdout split is fixed with `random_state=42`. Identical apartment fingerprints—district,
rooms, size, floor, building floors, and building type—are kept in one split. Approximately 80%
of feature groups form the development set and 20% form the protected test set, stratified by
district at group level. Model selection uses five-fold `StratifiedGroupKFold` only on development
data. All encoding/scaling stays inside scikit-learn pipelines.

```text
Public 2026 catalog → privacy-minimized snapshot → schema/range validation
       ↓
exact feature+target deduplication → feature fingerprint groups
       ↓
group-safe development/test split → group-safe five-fold model comparison
       ↓
protected unseen test evaluation → saved Random Forest pipeline
       ↓
validated apartment input → 2026 asking-price estimate + range warnings
```

### Training-only cross-validation

| Experiment | CV MAE | CV RMSE | CV R² |
|---|---:|---:|---:|
| Median baseline | $55,604 | $123,587 | -0.068 |
| Log Ridge | $38,301 | $105,755 | 0.219 |
| **Random Forest (selected)** | **$31,298** | **$80,394** | **0.556** |
| Gradient Boosting | $33,545 | $94,081 | 0.396 |

### Protected unseen test result

| Model | MAE | RMSE | R² | MAPE |
|---|---:|---:|---:|---:|
| Median baseline | $50,900 | $107,189 | -0.058 | 46.39% |
| **Random Forest** | **$27,195** | **$58,887** | **0.681** | **24.58%** |

Random Forest reduces MAE by **46.6%** versus baseline and meets all predefined thresholds. The
largest protected-test miss is a $1,000,000 Shayhontohur new-build listing predicted near $234,461.
Performance is much less reliable for high-end listings: Mirobod test MAE is about $52,143 and
Shayhontohur test MAE about $64,541. Full evidence is in `artifacts/metrics.json` and `reports/`.

## Reproduce locally

Python 3.10+ is required.

```bash
git clone https://github.com/DilnuraHamdamova/tashkent-house-price-predictor.git
cd tashkent-house-price-predictor
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m src.train
```

Run a resale-apartment prediction:

```bash
python -m src.predict \
  --district Chilonzor --size 70 --rooms 3 --level 3 --max-levels 5
```

The checked example returns approximately **$97,098 USD**. Add `--new-building` for a new build;
the checked equivalent returns approximately **$103,647 USD**. Values outside training ranges
or unseen districts produce warnings.

Run quality checks:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
ruff check src tests scripts
```

## Refresh the current snapshot

The committed snapshot makes evaluation reproducible. A later refresh creates a different dataset
and therefore requires retraining and re-reporting every metric:

```bash
python scripts/collect_current_listings.py apartment
python -m src.train
```

The collector follows the public catalog rather than disallowed API routes, uses a delay, and
checkpoints progress. Reconfirm source terms before each refresh.

## Colab demo

Open the Colab badge and choose **Runtime → Run all**. The notebook clones the repository when
needed, installs dependencies, loads the committed 2026 pipeline, predicts one resale and one
new-build example, and demonstrates invalid-floor validation without hidden notebook state.

## Limitations and responsible use

- The model estimates August 2026 advertisements; it is not a permanently live forecast.
- Asking price may differ materially from completed transaction price.
- User-entered listings can be stale, inaccurate, duplicated, or miscategorized.
- Same-feature grouping reduces leakage but cannot identify every relisted physical apartment.
- Exact address, condition, renovation, construction year, legal status, and amenities are absent.
- District slices vary sharply; negative R² in some districts means local reliability is weak.
- Yangihayot has no retained modeling rows and is out of distribution.
- Geographic price patterns may reproduce historical and current location inequality.
- Predictions require human review and recent comparable listings. Do not use this educational
  model for lending, taxation, legal appraisal, or high-stakes financial decisions.

## Author and assistance disclosure

**Dilnura Hamdamova** — Individual Project Track. AI coding assistance was used for scaffolding,
review, testing support, and documentation. The author remains responsible for verifying,
understanding, and defending every submitted claim.

## Defense evidence

The [official evidence matrix](docs/capstone_evidence_matrix.md),
[five-minute pitch](docs/defense_pitch_outline.md),
[complete defense-day guide](docs/defense_day_guide_uz.md),
[question bank](docs/defense_question_bank.md),
[final action plan](docs/final_action_plan.md), and
[clean-run record](reports/clean_run_check.md) form the defense preparation pack.
