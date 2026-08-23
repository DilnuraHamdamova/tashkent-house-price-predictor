# Official capstone evidence matrix — 2026 Tashkent apartments

## Eight criteria

| Criterion | What I claim | Exact evidence location | Why this is proof | Status | Gap / risk | Next action |
|---|---|---|---|---|---|---|
| 1. Problem Definition and Project Alignment — 10 / min 6 | The Individual Project estimates August 2026 Tashkent apartment asking prices for buyers, sellers, agents, and analysts. | `README.md` → “Problem and scope”; `submission/PROJECT_BRIEF.md` → problem/success criteria; `submission/Submission_Dilnura_Hamdamova.docx` | The README and revised brief name the user, regression task, inputs, USD asking-price target, thresholds, scope, and prohibited uses. | **YELLOW** | The revised brief exists, but retained mentor approval is still external evidence. | Student obtains and retains mentor approval before defense. |
| 2. Data and Preprocessing Pipeline — 15 / min 9 | Current public listing data is privacy-minimized, validated, deduplicated, and split by identical-feature group. | `data/README.md` → source/schema/quality; `scripts/collect_current_listings.py`; `reports/data_audit.md`; `src/data.py` → `load_dataset`; `src/model.py` → group split | These show the 22 Aug 2026 snapshot, 4,867 parsed rows, 257 invalid rows removed, 396 duplicates removed, 4,214 modeling rows, and 3,840 group-safe fingerprints. | **YELLOW** | HATA terms do not state an open-data redistribution license. | Retain written educational-use/redistribution permission, or provide snapshot privately under mentor guidance. Owner: Dilnura; before submission. |
| 3. Modeling and Experiments — 20 / min 12 | A median baseline and three meaningful regressors were compared; Random Forest was selected only by group-safe development CV MAE. | `reports/model_comparison.csv`; `artifacts/metrics.json` → `experiments`; `src/model.py` → `candidate_models`, `train_best_model`; `notebooks/02_experiments.ipynb` | Structured results show baseline, Log Ridge, Random Forest, Gradient Boosting, five-fold CV metrics, random seed, and selection rule. | **GREEN** | Controlled hyperparameters are not exhaustive tuning. | Explain reproducibility trade-off; propose nested tuning later. |
| 4. Evaluation and Error Analysis — 15 / min 9 | Random Forest was evaluated on 835 unseen rows from 768 protected groups with baseline comparison and slice/error analysis. | `reports/protected_test_metrics.csv`; `reports/largest_errors.csv`; `reports/district_metrics.csv`; `reports/results.md`; `artifacts/metrics.json` | Evidence includes MAE $27,195, RMSE $58,887, R² 0.681, MAPE 24.58%, baseline MAE $50,900, concrete residuals, district counts, and slice metrics. | **GREEN** | Luxury errors are large; some district R² values are negative. | Show the $1m Shayhontohur miss and explain that slice reliability is unequal. |
| 5. End-to-End Implementation and Delivery — 20 / min 12 | A raw apartment record passes validation, feature engineering, serialized preprocessing, and the trained model to a 2026 asking-price estimate. | `demo.ipynb` → setup/load/example/invalid-input cells; `src/predict.py`; `src/model.py` → `load_artifact`, `predict_price`; `artifacts/apartment_price_pipeline.joblib` | The same saved sklearn pipeline used after training returns about $97,098 for the checked resale example and rejects an impossible floor. | **GREEN** | Snapshot results will drift after August 2026. | State the snapshot date beside every “current” claim and define a refresh/retrain schedule. |
| 6. Documentation and Reproducibility — 10 / min 6 | A clean runtime can install, train, test, lint, and execute the focused inference demo. | `README.md` → reproduce/refresh/Colab; `requirements.txt`; `reports/clean_run_check.md`; `.github/workflows/ci.yml`; GitHub Actions run `32561644942` | Commands, pinned ranges, tests, collector, saved snapshot, pipeline, and successful current-revision public CI make the workflow inspectable. | **YELLOW** | The updated 2026 notebook still needs a named fresh-Colab reviewer. | Peer runs Colab and records name/date/result. Owner: Dilnura + peer; before defense. |
| 7. Responsible AI and Limitations — 5 / min 3 | The project distinguishes asking from sale price and documents recency, source noise, drift, missing features, geographic bias, privacy, and unsafe uses. | `README.md` → limitations; `data/README.md` → target/limitations; `reports/results.md` → district slices | These are project-specific limitations tied to observed data and errors, not generic AI warnings. | **GREEN** | Bias is diagnosed through performance variation, not causal fairness analysis. | Do not claim fairness or causality; require human review and comparables. |
| 8. Presentation, Demo, and Q&A — 5 / min 3 | A fixed five-minute route, working demo path, appendix evidence, and evidence-anchored question bank are prepared. | `presentation/Tashkent_Apartment_Price_Defense.pptx`; `docs/defense_pitch_outline.md`; `docs/defense_question_bank.md`; `docs/final_action_plan.md` | The route includes user/task, data/models, unseen result, baseline, failure, limitation, demo, next step, and Q&A pattern. | **YELLOW** | Timed rehearsal, peer challenge, and personal live defense are not yet performed. | Complete two timed rehearsals and one three-claim peer audit; record real results only. |

## Essential-requirement checklist

| Essential requirement | Status | Exact evidence / blocker |
|---|---|---|
| Overall score at least 60/100 | **YELLOW** | Official score occurs at defense; repository evidence covers every criterion but does not guarantee a score. |
| Real trained model, not external API only | **GREEN** | `artifacts/apartment_price_pipeline.joblib`; `src/model.py`; `artifacts/metrics.json`. |
| Evaluation on unseen data | **GREEN** | `reports/protected_test_metrics.csv`; group-safe 835-row protected test in `artifacts/metrics.json`. |
| Working end-to-end demo | **GREEN locally / YELLOW externally** | `demo.ipynb`, `src/predict.py`; named fresh-Colab review still required. |
| Reproduction instructions | **GREEN** | `README.md` → reproduce locally, refresh snapshot, Colab demo. |
| Student attends and answers defense | **YELLOW** | Only Dilnura can attend and answer personally; cannot be pre-completed. |

## Three-claim “Show Me Where” challenge

| # | High-risk claim | Exact proof shown | Pass/fail + missing context | Next action |
|---:|---|---|---|---|
| 1 | “The result is current 2026 asking-price evidence.” | `data/apartment_listings_2026.csv` → dates/timestamp; `data/README.md` → source/snapshot | PASS / FAIL: __________ | ____________________ |
| 2 | “Unseen evaluation is protected from identical-feature leakage.” | `src/model.py` → feature-group split and `StratifiedGroupKFold`; `artifacts/metrics.json` → group counts | PASS / FAIL: __________ | ____________________ |
| 3 | “The model beats baseline but fails on luxury listings.” | `reports/protected_test_metrics.csv`; first row of `reports/largest_errors.csv` | PASS / FAIL: __________ | ____________________ |

Partner name: ____________________  My role first: Owner / Challenger  Date: __________

## Readiness gate

**Current status: YELLOW.** Technical model/evaluation evidence is ready. Remaining blockers are
source-use confirmation, fresh external Colab/CI evidence, timed rehearsal, peer challenge, and
personal defense attendance. None may be marked complete without real evidence.
