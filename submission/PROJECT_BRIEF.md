# Individual Project Brief — 2026 revision

## Project information

- **Student:** Dilnura Hamdamova
- **Track:** Individual Project Track
- **Title:** Tashkent Apartment Listing Price Predictor
- **Repository:** https://github.com/DilnuraHamdamova/tashkent-apartment-price-predictor
- **ML task:** supervised tabular regression
- **Primary users:** buyers, sellers, agents, and analysts comparing current advertisements

## Problem

The project estimates an August 2026 Tashkent apartment's advertised asking price from district,
size, rooms, apartment floor, building floors, and new-build/resale status. The output supports
comparison and exploration only. It is not a verified completed sale price, legal appraisal,
loan/tax decision, or guaranteed price.

## Data

A privacy-minimized snapshot of public HATA Tashkent apartment-sale catalog pages was collected
on 22 August 2026. Listing dates range from 4–21 August 2026. The collector excludes identity,
contact details, descriptions, and images. The target `listing_price_usd` is the advertiser's
asking price, not a transaction label.

From 4,867 parsed complete-feature listings, fixed validity checks remove 257 obvious category,
currency, or unit errors. Removing 396 exact feature + target duplicates leaves 4,214 modeling
rows in 3,840 feature fingerprints. Source use and limitations are documented in
`data/README.md`; written redistribution permission is a recommended external confirmation.

## Success criteria

- Primary metric: MAE in USD.
- Supporting metrics: RMSE, R², and MAPE.
- Beat median-baseline protected-test MAE by at least 30%.
- Reach protected-test R² ≥ 0.60.
- Keep protected-test MAPE ≤ 25%.
- Accept a raw example through the saved preprocessing/model pipeline.

## Method

Identical `district + rooms + size + apartment floor + building floors + building type`
fingerprints remain in one split. Feature groups are split approximately 80/20 at district-
stratified group level. Five-fold `StratifiedGroupKFold` on development data compares:

1. Median Dummy Regressor
2. Log-transformed Ridge Regression
3. Random Forest Regressor
4. Gradient Boosting Regressor

Encoding/scaling remains inside each pipeline. Selection uses development CV MAE only. The chosen
model is evaluated once on protected groups, then refitted on all cleaned rows for inference.

## Results

Random Forest has the best CV MAE at $31,298 ± $3,252. On 835 protected rows from 768 unseen
feature groups it achieves:

- MAE: $27,195
- RMSE: $58,887
- R²: 0.681
- MAPE: 24.58%

Median-baseline test MAE is $50,900, so Random Forest improves MAE by 46.6% and meets all stated
thresholds. The largest failure is a $1,000,000 Shayhontohur listing predicted near $234,461.
Mirobod and Shayhontohur have high slice MAE, and some district slice R² values are negative.

## Delivered system

- Reproducible current-listing collector and committed snapshot
- Data validation, deduplication, fingerprint grouping, and feature engineering
- Baseline plus three trained candidate models
- Group-safe CV and protected unseen-test evaluation
- Saved preprocessing/model pipeline and structured metrics
- CLI prediction with validation and range/unseen-district warnings
- Focused Colab demo, development notebooks, tests, and CI configuration
- Error analysis, district slices, responsible-use documentation, deck, pitch, matrix, and Q&A

## Responsible AI and limitations

The model is a dated asking-price reference. Advertiser data can be stale, inaccurate,
misclassified, or duplicated. Exact building/location, condition, renovation, construction year,
legal status, and amenities are absent. Yangihayot is not represented. Geographic market patterns
may reproduce inequality, and district performance is unequal. Human review and recent comparable
listings are required; the model is prohibited for lending, taxation, legal appraisal, or other
high-stakes automated decisions.

The strongest improvement is verified transaction data with richer property features and a later
time-based holdout. Every future data refresh requires retraining and new reported metrics.

## Reproduction

```bash
python -m pip install -r requirements.txt
python -m src.train
python -m src.predict --district Chilonzor --size 70 --rooms 3 \
  --level 3 --max-levels 5
```

The checked resale example returns approximately $97,098 USD.
