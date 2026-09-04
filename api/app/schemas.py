from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

class TransactionRequest(BaseModel):
    """
    Input schema for one transaction prediction request.
    """

    transaction_id: Optional[str] = None
    actual_is_fraud: Optional[bool] = None
    features: Dict[str, Any]


class PredictionResponse(BaseModel):
    """
    Output schema returned by the fraud prediction API.
    """

    transaction_id: Optional[str]
    fraud_probability: float
    predicted_fraud: bool
    threshold: float
    risk_level: str
    inference_time_ms: float
    logged_to_database: bool

class PredictionRecord(BaseModel):
    """
    Response schema for one stored prediction record.
    """

    prediction_id: int
    transaction_id: int
    external_transaction_id: str | None
    fraud_probability: float
    predicted_fraud: bool
    threshold: float
    risk_level: str
    inference_time_ms: float | None
    predicted_at: datetime

    class Config:
        from_attributes = True


class AlertRecord(BaseModel):
    """
    Response schema for one fraud alert record.
    """

    alert_id: int
    transaction_id: int
    prediction_id: int
    external_transaction_id: str | None
    fraud_probability: float
    risk_level: str
    alert_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardMetrics(BaseModel):
    """
    Basic metrics for the fraud monitoring dashboard.
    """

    total_predictions: int
    total_alerts: int
    predicted_fraud_count: int
    average_fraud_probability: float
    critical_alerts: int
    high_alerts: int
    medium_alerts: int