# Field-Based Capstone Project Brief

## Project information

- **Student:** Dilnura Hamdamova
- **Track:** Field-Based Scenario — Real Estate
- **Title:** Tashkent House Price Predictor
- **Repository:** https://github.com/DilnuraHamdamova/tashkent-house-price-predictor
- **ML task:** supervised tabular regression
- **Primary user:** buyers, sellers, agents, and analysts seeking a historical reference estimate

## Problem

Tashkent's residential market has limited price transparency. This project tests whether observable listing attributes can provide a reproducible reference estimate of an apartment's advertised price. The model consumes district, size, rooms, floor information, and coordinates and returns a predicted 2019 listing price in USD.

The output supports comparison and exploration only. It is not a legal appraisal, current-market quote, loan decision, or guaranteed sale price.

## Data

The project uses the public [Real estate prices in Tashkent, Uzbekistan](https://www.kaggle.com/datasets/anvarnarz/tashkent-real-estate-2019) dataset. It contains 7,421 uybor.uz advertisements collected in 2019 and is published as CC0: Public Domain. The source workbook is committed as a CSV for reproducibility. Exact duplicates are removed before splitting, leaving 6,725 modeling rows.

The target is `price` in USD. Available features are `district`, `rooms`, `size`, `level`, `max_levels`, `lat`, and `lng`; `floor_ratio` is deterministically engineered. Approximate address is excluded to reduce memorization. No target-derived feature is used.

Main risks are duplicate advertisements, price/size outliers, sparse districts, historical data, asking-price labels, and missing condition/year/legal-status features. Decisions and limitations are recorded in `data/README.md` and `reports/data_audit.md`.

## Success criteria

- Primary metric: MAE in USD.
- Supporting metrics: RMSE, R², and MAPE.
- Beat the median baseline test MAE by at least 30%.
- Reach protected-test R² of at least 0.60.
- Keep protected-test MAPE at or below 25%.
- Accept a raw unseen example through the same saved preprocessing/model pipeline.

## Method

The de-duplicated data is split once into 80% development and 20% protected test data, stratified by district with `random_state=42`. Five-fold district-stratified cross-validation on development data compares:

1. Median Dummy Regressor (naive baseline)
2. Log-transformed Ridge Regression
3. Random Forest Regressor
4. Gradient Boosting Regressor

One-hot encoding and scaling are inside scikit-learn pipelines so preprocessing is fitted only on the relevant training fold. Selection uses CV MAE only. The chosen model is evaluated against the baseline on the protected test and then refitted on all rows for the final inference artifact.

## Results

Random Forest achieved the best CV MAE ($11,108 ± $745) and was selected. On 1,345 protected test rows it achieved:

- MAE: $10,573
- RMSE: $23,162
- R²: 0.745
- MAPE: 16.66%

The median baseline test MAE is $24,217, so the final model improves MAE by 56.3% and meets the predefined criteria. Mirobod luxury listings cause the largest residuals. Bektemir and Yangihayot slice results are unreliable due to very small sample sizes.

## Delivered system

- Reusable data validation and feature preparation in `src/data.py`
- Reproducible training/model selection in `src/train.py` and `src/model.py`
- Saved full preprocessing/model pipeline in `artifacts/house_price_pipeline.joblib`
- Structured experiment metadata in `artifacts/metrics.json`
- CLI inference with validation and out-of-distribution warnings in `src/predict.py`
- Focused, clean-runtime `demo.ipynb` for Google Colab
- EDA and experiment notebooks under `notebooks/`
- Dataset card, audit report, results, district slices, and error analysis
- Automated tests and GitHub Actions CI

## Responsible AI and limitations

Incorrect estimates may financially mislead a buyer or seller. A human must compare the output with recent listings and qualified local advice. Historical location effects may reproduce market inequality, and district-level accuracy varies with sample size. The model must not be used for lending, taxation, eligibility, legal appraisal, or automated decisions about individuals.

The strongest next step is current transaction data with building age, condition, renovation, legal status, amenities, and date. A time-aware holdout should replace a random holdout when multiple periods become available.

## Reproduction

From a clean Python 3.10+ environment:

```bash
python -m pip install -r requirements.txt
python -m src.train
python -m src.predict --district Chilonzor --size 70 --rooms 3 \
  --level 3 --max-levels 5 --lat 41.3002 --lng 69.2108
```

The README and Colab demo provide the complete assessed workflow.
