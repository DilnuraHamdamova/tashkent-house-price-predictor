# Data quality audit

The audit was run on `data/house_prices.csv` before model development.

| Check | Result | Decision |
|---|---:|---|
| Rows / columns | 7,421 / 9 | Sufficient for a compact tabular capstone |
| Missing required values | 0 | No imputation required for current data; pipeline still validates input |
| Exact duplicates | 696 | Remove before splitting to prevent train/test duplication leakage |
| Districts | 12 | Use one-hot encoding; stratify split and CV by district |
| Invalid floor (`level > max_levels`) | 0 | Reject such values during inference |
| Size range | 14–456 m² | Keep and emit out-of-range warnings at inference |
| Price range | $10,500–$800,000 | Keep rare listings; report RMSE and error cases |
| Coordinate ranges | 41.186–41.425, 69.149–69.589 | Validate geographic number ranges and warn outside training range |

## Issue log

1. **Duplicate advertisements:** could leak identical rows across random splits and inflate performance. Exact duplicates are removed before splitting.
2. **Uneven districts:** Bektemir has 8 source rows and Yangihayot 14, so their metrics are unstable. Split/CV are stratified, and the limitation is reported.
3. **Outliers:** 565 prices are outside the conventional 1.5×IQR fence. They may be luxury listings or errors; no automatic deletion is defensible without source verification.
4. **Address leakage/memorization:** approximate address has high cardinality. It is excluded; district and coordinates provide reusable location information.
5. **Historical asking prices:** values are 2019 advertisements in USD, not current sale prices. The system is explicitly an educational historical estimator.
6. **No hidden test tuning:** model selection uses only training-fold MAE. The protected test is evaluated after selection.
