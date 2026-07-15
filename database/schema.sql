-- FraudShield PostgreSQL Schema

-- Drop tables in reverse dependency order.
-- This makes it easier to rerun the schema during dev.
DROP TABLE IF EXISTS fraud_alerts;
DROP TABLE IF EXISTS predictions;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS model_runs;


-- Stores customer/account-level information.
CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,

    -- External ID could come from a real banking system later.
    external_customer_id VARCHAR(100) UNIQUE NOT NULL,

    -- Optional customer metadata.
    account_age_days INTEGER,
    country VARCHAR(100),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- Stores transaction-level data.
-- Each row represents one transaction being scored.
CREATE TABLE transactions (
    transaction_id BIGSERIAL PRIMARY KEY,

    -- Some transactions may not have a known customer yet.
    customer_id BIGINT REFERENCES customers(customer_id),

    -- Original transaction ID from the dataset or external system.
    external_transaction_id VARCHAR(100) UNIQUE,

    amount NUMERIC(12, 2),
    product_code VARCHAR(50),
    card_type VARCHAR(50),
    payment_type VARCHAR(50),

    payer_email_domain VARCHAR(150),
    recipient_email_domain VARCHAR(150),

    transaction_time TIMESTAMPTZ,

    -- Ground-truth label.
    is_fraud BOOLEAN,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- Stores each model version and its validation metrics.
-- This helps track which model was used and how it performed.
CREATE TABLE model_runs (
    model_run_id BIGSERIAL PRIMARY KEY,

    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) UNIQUE NOT NULL,

    algorithm VARCHAR(100),
    selected_threshold NUMERIC(6, 4),

    precision_score NUMERIC(8, 6),
    recall_score NUMERIC(8, 6),
    f1_score NUMERIC(8, 6),
    roc_auc NUMERIC(8, 6),
    pr_auc NUMERIC(8, 6),
    false_positive_rate NUMERIC(8, 6),

    training_rows INTEGER,
    validation_rows INTEGER,
    num_features INTEGER,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- Stores model predictions for transactions.
-- A transaction can have multiple predictions if different model versions score it.
CREATE TABLE predictions (
    prediction_id BIGSERIAL PRIMARY KEY,

    transaction_id BIGINT NOT NULL REFERENCES transactions(transaction_id),
    model_run_id BIGINT REFERENCES model_runs(model_run_id),

    fraud_probability NUMERIC(8, 6) NOT NULL,

    -- Final decision after applying the selected threshold.
    predicted_fraud BOOLEAN NOT NULL,

    -- Threshold used at prediction time.
    decision_threshold NUMERIC(6, 4),

    -- Useful production metric.
    inference_time_ms NUMERIC(10, 3),

    predicted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- Stores alerts created from high-risk predictions.
CREATE TABLE fraud_alerts (
    alert_id BIGSERIAL PRIMARY KEY,

    transaction_id BIGINT NOT NULL REFERENCES transactions(transaction_id),
    prediction_id BIGINT NOT NULL REFERENCES predictions(prediction_id),

    -- Example values: low, medium, high, critical
    risk_level VARCHAR(20),

    -- Example values: new, reviewing, confirmed_fraud, false_positive, closed
    alert_status VARCHAR(30) DEFAULT 'new',

    analyst_notes TEXT,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMPTZ
);


-- Indexes to improve lookup speed for common API queries.

-- Quickly find transactions by external ID.
CREATE INDEX idx_transactions_external_id
ON transactions(external_transaction_id);

-- Quickly filter transactions by fraud label.
CREATE INDEX idx_transactions_is_fraud
ON transactions(is_fraud);

-- Quickly sort/filter predictions by risk score.
CREATE INDEX idx_predictions_fraud_probability
ON predictions(fraud_probability);

-- Quickly filter alerts by status.
CREATE INDEX idx_fraud_alerts_status
ON fraud_alerts(alert_status);

-- Quickly filter alerts by risk level.
CREATE INDEX idx_fraud_alerts_risk_level
ON fraud_alerts(risk_level);