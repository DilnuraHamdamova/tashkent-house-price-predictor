# Defense question bank — 2026 apartment predictor

Answer pattern: **direct answer → exact evidence → limitation/next step**. Never guess.

| Likely question | My short answer | Evidence reference | Weak area / follow-up |
|---|---|---|---|
| What exactly does the target mean? | It is the USD asking price shown in an August 2026 advertisement, not a verified sale price. | `data/README.md` → “Target” | Negotiated transaction prices may differ. |
| Why is the project current? | The committed snapshot was collected 22 Aug 2026 and contains listing dates from 4–21 Aug 2026. | `data/apartment_listings_2026.csv` → `listing_date`, `collected_at_utc`; `reports/data_audit.md` | It is a dated snapshot, not permanently live. |
| Where did the data come from? | Rate-limited public HATA Tashkent apartment-sale catalog pages; no API, identity, contacts, descriptions, or images were collected. | `scripts/collect_current_listings.py`; `data/README.md` → source/privacy | HATA does not state an open redistribution license; written confirmation is recommended. |
| What cleaning did you perform? | I removed 257 rows outside conservative validity rules and 396 exact feature+target duplicates, leaving 4,214 rows. | `src/data.py` → `VALID_RANGES`, `load_dataset`; `artifacts/metrics.json` → `data_audit` | Rules may remove rare valid cases, but avoid outcome-driven IQR trimming. |
| How did you prevent duplicate leakage? | Identical district/rooms/size/floor/building-floor/type fingerprints stay in one holdout group and one CV fold. | `src/model.py` → group hash, group split, `StratifiedGroupKFold`; `artifacts/metrics.json` → group counts | Edited relistings can evade exact fingerprint matching. |
| What is the baseline? | Median Dummy Regressor, which ignores apartment features and predicts the development median. | `src/model.py` → `candidate_models`; `reports/model_comparison.csv` | It is deliberately simple as a minimum reference. |
| Why Random Forest? | It had the lowest group-safe development CV MAE: $31,298 versus $33,545 Gradient Boosting and $38,301 Log Ridge. | `reports/model_comparison.csv` | It is larger and less interpretable than Ridge. |
| Was test data used to select the model? | No. Selection used only five-fold development CV; the chosen model was evaluated once on protected groups. | `src/model.py` → `train_best_model`; `artifacts/metrics.json` → selection/split rules | Repeated future checking on the same test would weaken its protection. |
| What are the unseen-data results? | On 835 protected rows, MAE is $27,195, RMSE $58,887, R² 0.681, and MAPE 24.58%. | `reports/protected_test_metrics.csv` | Large luxury errors make RMSE much higher than MAE. |
| How much better is it than baseline? | Baseline MAE is $50,900; Random Forest reduces it by 46.6%. | `reports/protected_test_metrics.csv`; `reports/results.md` | Improvement does not make the model appraisal-grade. |
| What is the biggest failure? | A $1m Shayhontohur listing is predicted near $234,461, an error around $765,539. | `reports/largest_errors.csv`, first row | Missing condition/building/prestige may matter, but that cause is not verified. |
| Does it perform equally across districts? | No. Mirobod and Shayhontohur MAE are much higher, and Bektemir/Chilonzor slice R² is negative. | `reports/district_metrics.csv`; `reports/results.md` | Slice counts/metrics diagnose reliability, not fairness or causality. |
| Why no Yangihayot? | No Yangihayot row survived the current source/quality pipeline, so it is out of distribution. | `reports/data_audit.md` → representation; artifact `known_districts` | More representative source data is needed. |
| Why not use price per square metre? | It directly contains the target price and would leak the answer. | `reports/data_audit.md` → leakage risks; `src/data.py` → feature list | Area itself is retained as a legitimate input. |
| What happens with invalid input? | Impossible floors raise an error; unseen districts and values outside training ranges create warnings. | `demo.ipynb` invalid-input cell; `tests/test_data.py`, `tests/test_model.py` | Plausible-looking false combinations may still pass basic validation. |
| Can this predict tomorrow's exact sale price? | No. It estimates an August 2026 asking price from a dated snapshot. | `README.md` → limitations | Refresh/retrain and verified transactions are needed for later market use. |
| Is SHAP or an ensemble required? | No. The core rubric requires defensible models, unseen evaluation, and delivery; SHAP/ensembles are optional extensions. | `reports/model_comparison.csv`; official rubric | Add interpretation only after core evidence is stable. |
| How did AI assistance affect the project? | AI assisted scaffolding, review, testing, data-pipeline support, and documentation; assistance is disclosed and claims are reproducible. | `README.md` → assistance disclosure | The student must personally understand and defend every component. |

## Live rehearsal record

Question received: ________________________________________________________________

My live answer: __________________________________________________________________

What I must improve or verify: ____________________________________________________
