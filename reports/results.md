# 2026 experiment results and error analysis

## Protocol

After validation and exact feature + target deduplication, 4,214 rows remain in 3,840 identical-
feature groups. A fixed district-stratified group split creates 3,379 development rows (3,072
groups) and 835 protected test rows (768 groups). Five-fold `StratifiedGroupKFold` on development
data selects the lowest-MAE non-dummy model. Encoders and scalers are fit inside each fold.

## Cross-validation experiments

| Model | CV MAE ± SD | CV RMSE | CV R² |
|---|---:|---:|---:|
| Median baseline | $55,604 ± $6,428 | $123,587 | -0.068 |
| Log Ridge | $38,301 ± $6,705 | $105,755 | 0.219 |
| **Random Forest** | **$31,298 ± $3,252** | **$80,394** | **0.556** |
| Gradient Boosting | $33,545 ± $5,185 | $94,081 | 0.396 |

Random Forest is selected only from development CV MAE.

## Protected unseen test evaluation

| Model | MAE | RMSE | R² | MAPE |
|---|---:|---:|---:|---:|
| Median baseline | $50,900 | $107,189 | -0.058 | 46.39% |
| **Random Forest** | **$27,195** | **$58,887** | **0.681** | **24.58%** |

The selected model improves MAE by 46.6% and meets the predefined thresholds. The large gap
between MAE and RMSE shows that a small luxury tail still causes very large errors.

## Largest concrete failure

A Shayhontohur new-build listing with 3 rooms, 160 m², floor 2/9, and a $1,000,000 asking price is
predicted near $234,461: an underprediction of about $765,539. The dataset cannot establish why;
unobserved condition, exact building, amenities, prestige, or an inaccurate source price may be
responsible. These are hypotheses, not causal findings.

## District slices

| District | Test rows | MAE | R² | MAPE |
|---|---:|---:|---:|---:|
| Sergeli | 83 | $11,365 | 0.254 | 18.79% |
| Bektemir | 68 | $12,998 | -1.777 | 22.54% |
| Uchtepa | 77 | $13,422 | 0.563 | 22.44% |
| Yashnobod | 59 | $14,089 | 0.550 | 18.48% |
| Chilonzor | 68 | $16,940 | -0.659 | 25.72% |
| Olmazor | 86 | $18,287 | 0.490 | 20.97% |
| Mirzo Ulugbek | 42 | $21,811 | 0.549 | 19.59% |
| Yunusobod | 131 | $27,583 | 0.659 | 25.46% |
| Yakkasaroy | 78 | $37,397 | 0.463 | 25.78% |
| Mirobod | 31 | $52,143 | 0.506 | 36.04% |
| Shayhontohur | 112 | $64,541 | 0.668 | 33.74% |

Negative slice R² in Bektemir and Chilonzor means that, within those test slices, the model is
worse than predicting that slice's mean despite relatively modest MAE. Slice evidence must be
shown with sample counts and multiple metrics, not summarized as equal performance.

## Conclusion

The model is useful as an educational 2026 asking-price reference, not an appraisal. The clearest
improvements are verified transaction prices, exact neighborhood/building signal, condition,
renovation, construction year, legal status, and a later time-based holdout. A scheduled data
refresh would require retraining and new reported metrics rather than silently calling this
snapshot permanently current.
