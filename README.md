# tashkent-house-price-predictor
End-to-end machine learning project: predicting residential property prices in Tashkent using regression models. Includes data cleaning, EDA, feature engineering, model training (Linear Regression, Random Forest, XGBoost), evaluation, and a reproducible Colab demo
# 🏠 Tashkent House Price Predictor

End-to-end machine learning project: predicting residential property prices in Tashkent using regression models.

---

## 📌 Problem Statement

Tashkent is rapidly urbanizing, but buyers and sellers lack transparent tools to estimate fair property prices. Most rely on word-of-mouth or real estate agents. This project builds a data-driven regression model to predict house prices based on location, size, number of rooms, and other features.

**Goal:** Provide a reproducible, explainable ML pipeline that estimates house prices and highlights key price drivers.

---

## 📊 Dataset

**Source:** [House Prices in Tashkent](https://www.kaggle.com/datasets/dostonubaydullayev/house-prices-in-tashkent) (Kaggle)

**License:** Apache 2.0

**Key features:**
- Location (district / neighborhood)
- Total area (sqm)
- Number of rooms
- Floor and total floors
- Price (target variable)

**Dataset status:** Not yet downloaded. Will be added to `data/` during the Data Audit phase (C3).

---

## 📁 Project Structure

```
tashkent-house-price-predictor/
├── README.md                 # Project overview
├── PROJECT_STATUS.md         # Current progress
├── requirements.txt          # Dependencies
├── .gitignore                # Excluded files
├── data/
│   └── README.md             # Dataset source and license
├── notebooks/
│   ├── 01_data_audit.ipynb   # EDA and data quality checks
│   ├── 02_experiments.ipynb  # Model training and comparison
│   └── demo.ipynb            # Final inference demo
└── src/
    ├── preprocessing.py      # Data cleaning and feature engineering
    ├── train.py              # Model training scripts
    └── predict.py            # Inference functions
```
