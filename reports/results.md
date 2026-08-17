# Experiment results and error analysis

## Protocol

After removing exact duplicates, 6,725 rows remain. A fixed 80/20 district-stratified split creates 5,380 development rows and 1,345 protected test rows. Five-fold district-stratified CV on development data selects the lowest-MAE non-dummy model. Encoders and scalers are fit inside each fold through scikit-learn pipelines.

## Cross-validation experiments

| Model | Main hypothesis | CV MAE ± SD | CV RMSE | CV R² |
|---|---|---:|---:|---:|
| Median baseline | Reference price without features | $25,220 ± $1,030 | $47,276 | -0.081 |
| Log Ridge | Additive, regularized relationships; log target limits skew | $15,580 ± $1,230 | $47,449 | -0.248 |
| Random Forest | Non-linear interactions and local market segments | **$11,108 ± $745** | **$23,289** | **0.736** |
| Gradient Boosting | Sequential non-linear residual correction | $12,099 ± $660 | $25,473 | 0.685 |

Random Forest is selected solely from CV MAE.

## Protected test evaluation

| Model | MAE | RMSE | R² | MAPE |
|---|---:|---:|---:|---:|
| Median baseline | $24,217 | $47,235 | -0.062 | 38.56% |
| Random Forest | **$10,573** | **$23,162** | **0.745** | **16.66%** |

The selected model improves MAE by 56.3%. The gap between MAE and RMSE shows that a small number of luxury or anomalous listings still produce very large residuals.

## Largest errors

| District / property | Actual | Predicted | Absolute error | Interpretation |
|---|---:|---:|---:|---|
| Mirobod, 456 m², 10 rooms | $800,000 | $354,962 | $445,038 | Extreme luxury listing is underpredicted |
| Mirobod, 280 m², 2 rooms | $48,000 | $222,024 | $174,024 | Unusual size/room/price combination |
| Mirzo Ulugbek, 190 m², 4 rooms | $365,000 | $193,545 | $171,455 | High-end listing underpredicted |
| Mirobod, 110 m², 3 rooms | $295,000 | $141,854 | $153,146 | Likely unobserved condition/building premium |
| Mirobod, 152 m², 4 rooms | $380,000 | $228,085 | $151,915 | High-end listing underpredicted |

## District slices

Strong represented-district results include Chilonzor MAE $5,844 (R² 0.798), Uchtepa MAE $5,951 (R² 0.639), and Yunusobod MAE $9,332 (R² 0.731). Mirobod is hardest (MAE $23,531) because it contains several high-price outliers. Bektemir has only 2 test rows and Yangihayot 3, so their slice scores must not be generalized.

## Conclusion

The model meets the predefined thresholds but is not appraisal-grade. The clearest improvements would come from current transaction data plus building condition, construction year, renovation, legal status, and listing date. Repeated collection over time would also support a time-aware split and market adjustment.
