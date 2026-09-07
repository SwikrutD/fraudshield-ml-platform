# FraudShield Dashboard

This folder contains the Streamlit dashboard for the FraudShield ML platform.

## Purpose

The dashboard connects to the FastAPI backend and displays:

- Total predictions
- Total fraud alerts
- Predicted fraud count
- Average fraud probability
- Alert counts by risk level
- Recent prediction logs
- Recent fraud alerts

## Run Locally

Start the FastAPI backend first:

```bash
uvicorn api.app.main:app --reload