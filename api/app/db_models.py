from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Transaction(Base):
    """
    Stores transaction records scored by the API.
    """

    __tablename__ = "transactions"

    transaction_id = Column(BigInteger, primary_key=True, index=True)
    external_transaction_id = Column(String(100), unique=True, nullable=True)

    amount = Column(Numeric(12, 2), nullable=True)
    is_fraud = Column(Boolean, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ModelRun(Base):
    """
    Stores model version metadata.
    """

    __tablename__ = "model_runs"

    model_run_id = Column(BigInteger, primary_key=True, index=True)

    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), unique=True, nullable=False)
    algorithm = Column(String(100), nullable=True)

    selected_threshold = Column(Numeric(6, 4), nullable=True)

    precision_score = Column(Numeric(8, 6), nullable=True)
    recall_score = Column(Numeric(8, 6), nullable=True)
    f1_score = Column(Numeric(8, 6), nullable=True)
    roc_auc = Column(Numeric(8, 6), nullable=True)
    pr_auc = Column(Numeric(8, 6), nullable=True)
    false_positive_rate = Column(Numeric(8, 6), nullable=True)

    training_rows = Column(BigInteger, nullable=True)
    validation_rows = Column(BigInteger, nullable=True)
    num_features = Column(BigInteger, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Prediction(Base):
    """
    Stores fraud prediction outputs from the API.
    """

    __tablename__ = "predictions"

    prediction_id = Column(BigInteger, primary_key=True, index=True)

    transaction_id = Column(
        BigInteger,
        ForeignKey("transactions.transaction_id"),
        nullable=False
    )

    model_run_id = Column(
        BigInteger,
        ForeignKey("model_runs.model_run_id"),
        nullable=True
    )

    fraud_probability = Column(Numeric(8, 6), nullable=False)
    predicted_fraud = Column(Boolean, nullable=False)
    decision_threshold = Column(Numeric(6, 4), nullable=False)
    risk_level = Column(String(20), nullable=False)

    inference_time_ms = Column(Numeric(10, 3), nullable=True)

    predicted_at = Column(DateTime(timezone=True), server_default=func.now())


class FraudAlert(Base):
    """
    Stores alerts generated from medium/high/critical fraud predictions.
    """

    __tablename__ = "fraud_alerts"

    alert_id = Column(BigInteger, primary_key=True, index=True)

    transaction_id = Column(
        BigInteger,
        ForeignKey("transactions.transaction_id"),
        nullable=False
    )

    prediction_id = Column(
        BigInteger,
        ForeignKey("predictions.prediction_id"),
        nullable=False
    )

    risk_level = Column(String(20), nullable=False)
    alert_status = Column(String(30), default="new")
    analyst_notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)