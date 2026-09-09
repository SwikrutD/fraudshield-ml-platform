# FraudShield ML Platform

FraudShield is an end-to-end machine learning platform for detecting fraudulent financial transactions. The project uses the IEEE-CIS Fraud Detection dataset to train, evaluate, explain, and deploy a fraud detection model through a production-style architecture.

The platform includes data exploration, feature engineering, model training, threshold optimization, SHAP explainability, distribution shift analysis, a FastAPI prediction service, PostgreSQL prediction logging, and a Streamlit fraud monitoring dashboard.

---

## Project Overview

Fraud detection is a highly imbalanced classification problem where fraudulent transactions are rare compared with legitimate transactions. Because of this, accuracy alone is not a useful evaluation metric.

This project focuses on practical fraud detection goals:

- Detecting a high percentage of fraud cases
- Controlling the false-positive rate
- Ranking high-risk transactions for analyst review
- Explaining model predictions with SHAP
- Logging predictions and fraud alerts for monitoring

---

## Dataset

This project uses the IEEE-CIS Fraud Detection dataset.

The main training dataset contains more than 590,000 transaction records and hundreds of anonymized transaction, card, address, email, and identity-related features.

For realistic evaluation, the data was split chronologically:

- Earlier 80% of transactions: training set
- Later 20% of transactions: validation set

This avoids overly optimistic results from random splitting and better simulates future transaction scoring.

---

## Key Results

### Baseline Model

A Logistic Regression baseline was trained first to establish a benchmark.

Baseline performance:

- Fraud precision: 0.090
- Fraud recall: 0.790
- Fraud F1-score: 0.160
- ROC-AUC: 0.829
- PR-AUC: 0.189

### Final XGBoost Model

The final model used XGBoost with engineered numerical features and class-imbalance handling.

Final model ranking performance:

- ROC-AUC: 0.907
- PR-AUC: 0.518

At the selected business threshold of `0.325`, the model achieved:

- Fraud recall: 0.804
- Fraud precision: 0.163
- False-positive rate: 0.148
- Fraud F1-score: 0.270

This threshold was selected because it detected more than 80% of fraud cases while keeping the false-positive rate below 15%.

### High-Risk Transaction Ranking

The model was also evaluated by ranking transactions by predicted fraud probability.

Results from the highest-risk validation transactions:

- Top 10 highest-risk predictions: 100% fraud
- Top 100 highest-risk predictions: 92% fraud

This shows that the model is especially useful for prioritizing suspicious transactions for fraud analyst review.

---

## Machine Learning Workflow

The project follows a full data science workflow:

1. Exploratory data analysis
2. Data cleaning
3. Baseline Logistic Regression modeling
4. XGBoost modeling
5. Threshold tuning
6. Feature engineering
7. Feature subset testing
8. Hyperparameter tuning
9. SHAP explainability
10. Distribution shift analysis
11. Model artifact saving
12. API deployment
13. Prediction logging
14. Dashboard monitoring

---

## Feature Engineering

Engineered features included:

- Transaction time features
- Transaction amount log transformation
- Night transaction indicator
- Round amount indicator
- High amount indicator
- Card frequency features
- Email domain indicators
- Address comparison features

The final model used the engineered numerical feature set.

---

## Explainability

SHAP was used to explain model behavior at both the global and individual transaction level.

The explainability workflow included:

- XGBoost feature importance
- SHAP global feature importance
- SHAP beeswarm plot
- SHAP waterfall plots for individual high-risk and low-risk transactions

This allows the model to support fraud review instead of acting as a black-box classifier.

---

## Distribution Shift Analysis

A distribution shift analysis was performed between the chronological training and validation periods.

Key findings:

- Training fraud rate: 3.5135%
- Validation fraud rate: 3.4409%

The target distribution remained stable across time.

Population Stability Index was also calculated for selected features. Most checked features showed low shift, while `transaction_day` showed significant shift because the validation set intentionally represents a later time period.

This supports the use of chronological validation and provides a foundation for future drift monitoring.

---

## System Architecture

```text
Raw Transaction Data
        ↓
Data Cleaning and Feature Engineering
        ↓
XGBoost Fraud Detection Model
        ↓
Threshold Optimization
        ↓
Saved Model Artifacts
        ↓
FastAPI Prediction Service
        ↓
PostgreSQL Prediction Logging
        ↓
Fraud Alert Generation
        ↓
Streamlit Monitoring Dashboard