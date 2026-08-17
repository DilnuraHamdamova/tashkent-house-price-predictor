# Clean-runtime reproduction record

## Automated and local checks

Date checked: 17 August 2026 (Asia/Samarkand)

1. Created a new Python 3.12 virtual environment under `/tmp`.
2. Installed only the committed dependency instructions:

   ```bash
   python -m pip install -e . -r requirements-dev.txt
   ```

3. Loaded `data/house_prices.csv`: 7,421 source rows, 696 exact duplicates removed, 6,725 modeling rows.
4. Loaded `artifacts/house_price_pipeline.joblib` and ran:

   ```bash
   python -m src.predict --district Chilonzor --size 70 --rooms 3 \
     --level 3 --max-levels 5 --lat 41.3002 --lng 69.2108
   ```

   Observed output: `Estimated listing price: $53,532 USD`.

5. Executed every code cell in `notebooks/01_data_audit.ipynb`, `notebooks/02_experiments.ipynb`, and `demo.ipynb` sequentially. All completed; the demo also produced the expected invalid-floor error.
6. Ran `python -m pytest`: 6 tests passed.
7. Ran `ruff check src tests`: all checks passed.

## Public CI evidence

GitHub Actions run [32002361933](https://github.com/DilnuraHamdamova/tashkent-house-price-predictor/actions/runs/32002361933) checked out a fresh copy on Ubuntu/Python 3.11, installed the project and dev requirements, passed lint, and passed all six tests.

## Honest remaining reproduction action

The notebook code and clone/install route were tested from a clean local runtime, but a named peer/mentor has not yet recorded a fresh browser-based Google Colab run. Before defense, one reviewer should click the README Colab badge, choose **Runtime → Run all**, record the date/result here, and report any hidden-state or access issue.

- Peer/reviewer: ____________________
- Date: ____________________
- Result: PASS / FAIL
- Notes: ____________________
