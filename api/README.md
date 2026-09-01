# FraudShield ML API

This folder contains the FastAPI backend for the FraudShield fraud detection platform.

## Endpoints

- `GET /`: API status message
- `GET /health`: health check endpoint
- `POST /predict`: scores a transaction and returns fraud probability, predicted fraud label, threshold, and risk level

## Model Artifacts

The API loads the saved model artifacts from:

- `models/fraud_xgboost_v1/model.joblib`
- `models/fraud_xgboost_v1/features.json`
- `models/fraud_xgboost_v1/metadata.json`

## Run Locally

```bash
uvicorn api.app.main:app --reload