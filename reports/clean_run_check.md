# Reproduction and verification record

## Current local checks

Date checked: 22 August 2026 (Asia/Samarkand)

1. Loaded `data/apartment_listings_2026.csv`: 4,867 complete-feature source listings.
2. Applied the documented validation and duplicate policy: 257 invalid/out-of-scope rows and 396 exact feature-and-target duplicates were removed, leaving 4,214 modeling rows in 3,840 feature-fingerprint groups.
3. Trained the candidates through the committed command:

   ```bash
   python -m src.train
   ```

   The protected-test split contained 835 rows in 768 groups. Random Forest was selected from development cross-validation and achieved MAE `$27,195`, RMSE `$58,887`, R² `0.681`, and MAPE `24.58%` on the protected test set. The median baseline MAE was `$50,900`.
4. Confirmed that identical feature fingerprints do not cross either the development/test boundary or cross-validation folds: both recorded overlap checks equal zero.
5. Loaded `artifacts/house_price_pipeline.joblib` and ran:

   ```bash
   python -m src.predict --district Chilonzor --size 70 --rooms 3 \
     --level 3 --max-levels 5
   ```

   Observed output: `Estimated listing price: $97,098 USD`.
6. Executed every code cell in `notebooks/01_data_audit.ipynb`, `notebooks/02_experiments.ipynb`, and `demo.ipynb` sequentially in a fresh process. All completed; the demo also produced the expected invalid-floor validation error.
7. Ran `python -m pytest`: 8 tests passed.
8. Ran `ruff check src tests scripts`: all checks passed.

## External reproduction status

The repository's current code, notebooks, dataset snapshot, model artifact, and instructions pass
local verification. GitHub Actions run
[32561644942](https://github.com/DilnuraHamdamova/tashkent-house-price-predictor/actions/runs/32561644942)
checked commit `e31bc95` and completed successfully on 22 August 2026.

A named peer or mentor has also not yet recorded a browser-based Google Colab run. Before defense, one reviewer should click the README Colab badge, choose **Runtime -> Run all**, record the date/result here, and report any hidden-state or access issue.

- Current-revision public CI URL: https://github.com/DilnuraHamdamova/tashkent-house-price-predictor/actions/runs/32561644942
- Peer/reviewer: ____________________
- Date: ____________________
- Colab result: PASS / FAIL
- Notes: ____________________
