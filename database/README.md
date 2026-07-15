# Database

This folder contains the PostgreSQL schema for the FraudShield ML platform.

## Tables

- `customers`: customer/account-level records
- `transactions`: transaction records to be scored
- `model_runs`: model version and metric metadata
- `predictions`: fraud probability outputs from the ML model
- `fraud_alerts`: alert workflow for high-risk transactions

The schema is designed for a production-style fraud monitoring system where the model predictions are stored, tracked and reviewed.