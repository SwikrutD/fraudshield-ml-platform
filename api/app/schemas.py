from pydantic import BaseModel
from typing import Dict, Any, Optional


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