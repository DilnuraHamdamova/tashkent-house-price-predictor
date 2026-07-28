# Project Brief — Submission

Project: Tashkent House Price Predictor
Repository: DilnuraHamdamova/tashkent-house-price-predictor

## Summary
A supervised regression solution to estimate residential property prices in Tashkent from property features. The project provides a reproducible pipeline, evaluation results, and a demo for inference.

## Dataset
- Name: "House Prices in Tashkent" (Kaggle)
- License: Apache 2.0
- Key fields used: Location (district), Total_Area_sqm, Rooms, Floor, Total_Flats, Price (target)

## Models used
- Baseline: Linear Regression (interpretable baseline)
- Tree-based models: Random Forest Regressor and XGBoost Regressor (primary models for final comparison)

## Preprocessing & Features
- Categorical encoding for `Location` (one-hot or target encoding in experiments)
- Numeric features: scaling where required for baseline models
- Outlier handling and basic cleaning, with checks for missing values
- No features derived from the target (avoids leakage)

## Evaluation
- Train/test split: 80% train / 20% test; cross-validation on training set for hyperparameter tuning
- Primary metrics: RMSE (primary) and R²
- Additional analysis: performance by district and feature importance inspection

## Deliverables (included in repo)
- Notebook: `demo.ipynb` (end-to-end pipeline and demo inference)
- Requirements: `requirements.txt` (pinned dependencies)
- Saved model: `model.pkl` (best-performing model and preprocessing pipeline)
- Data docs: `data/README.md` (dataset source, license, and preprocessing notes)
- This brief: `submission/PROJECT_BRIEF.md`

## Limitations & Notes
- Geographic scope is limited to Tashkent; model may not generalize outside the dataset area
- Dataset size and feature scope limit granularity of predictions (no building year, condition, or exact address-level features)
- Recommend collecting more labeled data and additional features (year built, renovation status) to improve accuracy

## How to run (quick)
1. Install dependencies: `pip install -r requirements.txt`
2. Open `demo.ipynb` in Colab or locally and run cells to reproduce training and inference
3. Use the provided `predict()` function in the notebook to get price estimates on new property inputs

---

If you'd like, I can (a) add a short one-page PDF version, (b) update the readme to link to this brief, or (c) include the model's final RMSE and R² values here once you confirm which model was selected as final.