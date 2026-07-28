# FIELD-BASED CAPSTONE SCENARIO
Tashkent House Price Predictor
Real Estate | Technical Project Brief

Track: Field-Based Scenario
Client: Real estate stakeholders in Tashkent (buyers, sellers, agents, analysts)
Purpose: Design and implement a supervised machine learning solution that predicts residential property prices in Tashkent to improve price transparency and support data-driven decisions in the local [...]

---

1. Client Background
--------------------
Tashkent is undergoing rapid urbanization, producing a dynamic and often opaque real estate market. Buyers, sellers, and local agents often rely on anecdotal knowledge and agent estimates when val[...]

2. Business Problem
-------------------
There is no standardized, data-driven method to estimate fair market prices for residential properties in Tashkent. This information asymmetry leads to:
- Buyers possibly overpaying due to lack of comparable objective estimates.
- Sellers underpricing or being unable to justify their asking price.
- Agents and analysts relying on intuition rather than reproducible analysis.

The business need is a transparent, reproducible pricing tool that estimates property values from observable characteristics to reduce information asymmetry and increase market confidence.

3. Requested Solution
---------------------
Develop a supervised regression solution to predict residential property prices in Tashkent using the publicly available "House Prices in Tashkent" dataset (Kaggle, Apache 2.0). Deliverables shoul[...]
- A reproducible end-to-end Colab notebook demonstrating data processing, model training, evaluation, and inference.
- A saved model and preprocessing pipeline for inference (model.pkl).
- Documentation (dataset license/notes, evaluation results, limitations).
- A demo inference helper (e.g., predict() function) for quick price estimates on new properties.

4. Available Information
------------------------
Dataset: "House Prices in Tashkent" (Kaggle) — Apache 2.0 license.

Key fields available and used:
- Location: District or neighborhood (categorical)
- Total_Area_sqm: Total area in square meters (numeric)
- Rooms: Number of rooms (numeric)
- Floor: Floor number of the unit (numeric)
- Total_Flats (Total number of floors in the building) (numeric)
- Price: Target variable (numeric, UZS)

Notes:
- Data is publicly available and contains anonymized property listings.
- No personally identifiable information (PII) is present.
- Additional metadata (if present) must be reviewed for leakage risk.

5. Data & Problem Discovery — Complete Before Modeling
------------------------------------------------------

Decision / Question | Student Response
:--- | :---
Selected dataset and source | Dataset: "House Prices in Tashkent" (Kaggle). Source: Kaggle dataset page. License: Apache 2.0.
What does one record / sample represent? | One record = single residential property listing in Tashkent with features and listed/recorded price.
Proposed target or ML objective | Supervised regression. Target: Price (UZS). Objective: Predict numeric price from property features.
Key information available at prediction / inference time | Location (district), Total_Area_sqm, Rooms, Floor, Total_Flats — all available at inference and do not rely on the target.
Main data quality issues | Check for: missing values, inconsistent district names/spellings, outliers (area, price), invalid floor values, and imbalanced district representation. Numeric features [...]
Potential leakage risks | Avoid features derived from the target (e.g., price per sqm). If any target-derived encodings or post-sale metadata exist, exclude them to prevent leakage.
Privacy / fairness / licensing concerns | Dataset is under Apache 2.0 and anonymized. Evaluate fairness by inspecting per-district error distributions — ensure model does not systematically unde[...]

6. Technical Proposal — Complete Before Full Implementation
-----------------------------------------------------------

Decision / Question | Student Response
:--- | :---
ML problem formulation | Supervised regression: learn mapping f(features) → Price.
Proposed baseline | Linear Regression (Ordinary Least Squares). Use Ridge variant as a robust baseline if regularization helps.
Main modeling approach(es) to investigate | Linear Regression (baseline), Random Forest Regressor (tree ensemble), XGBoost Regressor (gradient boosting). Compare models and consider ensembling if [...]
Data splitting / validation strategy | Hold-out: 80% train / 20% test. On training set use k-fold cross-validation (e.g., 5-fold) for hyperparameter tuning. Consider grouped or stratified splittin[...]
Primary evaluation metric(s) and why | Primary: Root Mean Squared Error (RMSE) — interpretable in UZS. Secondary: R-squared (R²) and Mean Absolute Error (MAE) for outlier-robustness. Report per[...]
Expected inference input | JSON or dict with: { Location, Total_Area_sqm, Rooms, Floor, Total_Flats }. Input is preprocessed with same pipeline used in training.
Expected inference output | Single numeric predicted Price (UZS). Additionally, return a confidence estimate (e.g., prediction interval or a flag if input is out-of-distribution).
Main technical risks / assumptions | Dataset representativeness for current market; limited features (no year built, condition) constrain granularity; sparse data in some districts may limit accur[...]

7. Functional Requirements
--------------------------

Requirement | How the project satisfies it
:--- | :---
Provide a quantitative price estimate for a property | Regression model returns numeric price prediction in UZS for given features.
Reproducibility and explainability | Provide Colab notebook, pinned requirements.txt, saved preprocessing+model pipeline. Use feature importance and SHAP to explain model behavior.
Easy to use and test | Provide demo.ipynb with a predict() helper function and example inputs; include sample scripts showing how to load model.pkl and run predictions.
Useful for client context | Estimates are in local currency with RMSE context and per-district reliability notes to help buyers, sellers, and agents use results appropriately.

8. Expected Deliverables
------------------------

Deliverable | How it will be delivered
:--- | :---
Working ML solution | demo.ipynb (Google Colab) implementing end-to-end pipeline and demo inference.
Trained model or ML pipeline | model.pkl (scikit-learn Pipeline or serialized artifact bundling preprocessing + model).
Dataset documentation | data/README.md with dataset source URL, license (Apache 2.0), field descriptions, and preprocessing decisions.
Evaluation results | Test-set RMSE, MAE, R² for Linear Regression, Random Forest, and XGBoost; cross-validation summaries and per-district error analysis.
Inference interface | predict() function in demo.ipynb; optional small Gradio demo if requested.
Reproducible repository | Full GitHub repo with notebooks, requirements.txt, README, saved model, and submission/PROJECT_BRIEF.md.
Limitations & recommendations | Documented section outlining limits (geography, features), fairness checks, and suggestions for future data collection and model improvements.

9. Acceptance Criteria
----------------------

Acceptance Criterion | How the project satisfies it
:--- | :---
Processes previously unseen input | Saved preprocessing pipeline + model can accept new property features and return a price prediction.
Output is meaningful for the client | Predictions are presented in UZS with RMSE context and per-district reliability notes.
Methodology and evaluation are explainable | Notebook documents preprocessing, modeling, tuning, and evaluation; includes feature importance and SHAP visualizations.
Reproducible | Colab notebook, pinned dependencies, and fixed random seeds are provided to reproduce experiments.
Known limitations, risks, and assumptions documented | Brief and data/README.md include limitations, representativeness concerns, and potential biases.
Implementation runs per documentation | README contains step-by-step instructions to reproduce training and inference locally or in Colab.

10. Constraints
---------------

In Scope (What this project includes)
- Build and evaluate regression models (Linear Regression, Random Forest, XGBoost) on the Kaggle "House Prices in Tashkent" dataset.
- Provide a reproducible Colab notebook and serialized model/pipeline for inference.
- Perform basic fairness and per-district error analysis to identify significant bias or blind spots.

Out of Scope (What this project does NOT include)
- Full production deployment (no hosted web or mobile application).
- Real-time integration with live listing APIs.
- Detailed appraisal-level features (e.g., interior condition, exact address-level micro-pricing) unless additional data is provided.

11. Questions You Must Resolve
------------------------------
1. Which features are most important for predicting house prices?  
   - Answer approach: compute feature importance (Random Forest / XGBoost) and SHAP values; surface top 5 drivers.

2. How well does the model generalize across different districts in Tashkent?  
   - Answer approach: per-district RMSE/MAE and bias analysis; produce maps or tables showing district-level errors.

3. How many and which features are sufficient?  
   - Answer approach: incremental feature selection and model comparisons; consider recursive feature elimination or L1-regularized baselines.

4. What is an acceptable prediction error for practical use?  
   - Answer approach: contextualize RMSE relative to median/mean price and stakeholder expectations; propose thresholds for “useful” vs “warning” predictions.

5. How can predictions be explained to a non-technical user?  
   - Answer approach: present the top 3 contributing features for a specific prediction, show expected error range, and include clear textual guidance in the demo.

6. How to detect and handle out-of-distribution inputs?  
   - Answer approach: implement input validation and range checks; warn when inputs fall outside training ranges and avoid overconfident intervals.

---

Appendix — Quick Implementation Notes
-------------------------------------
- Preprocessing pipeline:
  - Clean and normalize district names, handle missing values, validate floor ≤ total_floors.
  - Numeric scaling for Linear Regression (StandardScaler); tree models not required to scale.
  - Encode Location: One-Hot Encoding for interpretable baselines; consider target (mean) encoding with nested CV to avoid leakage for tree-based models if district cardinality is high.
  - Use sklearn Pipeline to bundle preprocessing + model for safe serialization.

- Baselines & models:
  - Baseline: Linear Regression (OLS) and Ridge variant for stability.
  - Tree-based: RandomForestRegressor (sklearn) and XGBoost XGBRegressor.
  - Hyperparameter search: RandomizedSearchCV or GridSearchCV with 5-fold CV on training set.

- Explainability:
  - Feature importance (tree impurity and permutation importance).
  - SHAP values for local explanations (XGBoost/RandomForest).

- Evaluation reporting:
  - Report RMSE, MAE, R² on hold-out test set.
  - Provide cross-validation means and stds.
  - Present per-district error table and visualization (boxplots or bar charts).

- Reproducibility:
  - Pinned dependencies in requirements.txt.
  - Fixed random seeds for model training and CV folds.
  - Step-by-step README with instructions to run demo.ipynb in Colab.
