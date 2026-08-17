# Tashkent House Price Predictor

[![CI](https://github.com/DilnuraHamdamova/tashkent-house-price-predictor/actions/workflows/ci.yml/badge.svg)](https://github.com/DilnuraHamdamova/tashkent-house-price-predictor/actions/workflows/ci.yml)
[![Open demo in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DilnuraHamdamova/tashkent-house-price-predictor/blob/main/demo.ipynb)

An end-to-end regression capstone that estimates the advertised price of a Tashkent apartment from its district, size, room/floor information, and coordinates. The repository includes data documentation, reproducible model comparison, protected-test evaluation, a saved inference pipeline, input validation, tests, and a clean Google Colab demo.

## Problem and scope

Buyers, sellers, and real-estate analysts need a quick reference estimate in a market with limited price transparency. The ML task is supervised regression:

- **Input:** district, size (m²), rooms, apartment level, building levels, latitude, longitude.
- **Output:** estimated listing price in **USD**.
- **Primary metric:** MAE, because its dollar error is easy to interpret.
- **Supporting metrics:** RMSE, R², and MAPE.
- **Success criterion:** beat the median baseline test MAE by at least 30%, reach test R² ≥ 0.60, and test MAPE ≤ 25%.
- **Non-goals:** official appraisal, sale-price guarantee, live-market forecast, exact-address valuation, or autonomous financial decision-making.

## Data

The committed `data/house_prices.csv` contains 7,421 Tashkent apartment listings scraped from uybor.uz in 2019. It comes from Kaggle's [Real estate prices in Tashkent, Uzbekistan](https://www.kaggle.com/datasets/anvarnarz/tashkent-real-estate-2019), published under **CC0: Public Domain**. Prices are USD asking prices, not UZS and not verified transaction prices.

The training loader removes 696 exact duplicates, leaving 6,725 rows. There are 12 districts and no missing values in required fields. Exact address is excluded to reduce memorization; district and coordinates retain location signal. See [data/README.md](data/README.md) and [reports/data_audit.md](reports/data_audit.md).

## Method

The split is fixed with `random_state=42`: 80% development data and a protected 20% test set, stratified by district. Model selection uses only five-fold district-stratified cross-validation on the development split. All encoders/scalers live inside scikit-learn pipelines, preventing preprocessing leakage. After final test evaluation, the selected pipeline is refitted on all de-duplicated rows for inference.

| Experiment | CV MAE (USD) | CV RMSE (USD) | CV R² |
|---|---:|---:|---:|
| Median baseline | 25,220 | 47,276 | -0.081 |
| Log Ridge | 15,580 | 47,449 | -0.248 |
| **Random Forest (selected)** | **11,108** | **23,289** | **0.736** |
| Gradient Boosting | 12,099 | 25,473 | 0.685 |

### Protected test result

| Model | MAE (USD) | RMSE (USD) | R² | MAPE |
|---|---:|---:|---:|---:|
| Median baseline | 24,217 | 47,235 | -0.062 | 38.56% |
| **Random Forest** | **10,573** | **23,162** | **0.745** | **16.66%** |

The selected model reduces MAE by 56.3% versus the baseline and meets all stated success criteria. Large errors remain for rare luxury/outlier listings; the worst test miss is a $800,000 Mirobod listing predicted near $354,962. District slices with very few examples (especially Bektemir and Yangihayot) are not reliable. Full metrics are in [artifacts/metrics.json](artifacts/metrics.json) and analysis is in [reports/results.md](reports/results.md).

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

Run a prediction:

```bash
python -m src.predict \
  --district Chilonzor --size 70 --rooms 3 \
  --level 3 --max-levels 5 --lat 41.3002 --lng 69.2108
```

The checked example returns approximately `$53,532 USD`; small differences can occur across supported dependency versions. Unknown districts or values outside the training range produce a warning.

Run quality checks:

```bash
python -m pip install -r requirements-dev.txt
pytest
ruff check src tests
```

## Colab demo

Click the Colab badge above and choose **Runtime → Run all**. The notebook clones this repository when necessary, installs dependencies, loads the committed model, validates one raw example, and produces a prediction without hidden notebook state. `notebooks/01_data_audit.ipynb` and `notebooks/02_experiments.ipynb` document development; `demo.ipynb` is the focused final demonstration.

## Repository structure

```text
├── data/                       # Dataset and dataset card
├── notebooks/                  # EDA and experiment notebooks
├── artifacts/                  # Saved pipeline and metrics
├── reports/                    # Data audit, results, error analysis
├── src/                        # Reusable load/train/predict code
├── tests/                      # Validation and inference tests
├── submission/                 # Project brief and LMS submission document
├── demo.ipynb                  # Clean Colab inference demo
├── requirements.txt
└── README.md
```

## Limitations and responsible use

- Data represents 2019 advertisements, so the model is not calibrated to current market prices.
- Asking price may differ from final sale price.
- Sparse districts have unstable slice metrics; the model should not be used to compare or rank residents.
- Important factors such as renovation quality, building age, legal status, and market date are absent.
- Coordinates can create location bias, and the model may reproduce historical price inequalities.
- Predictions require human review and comparable listings. Do not use this educational model for lending, taxation, legal appraisal, or high-stakes financial decisions.

## Author and assistance disclosure

**Dilnura Hamdamova** — Individual capstone project. AI coding assistance was used for scaffolding, review, testing support, and documentation. The author remains responsible for verifying, understanding, and defending the submitted work.
