from pydantic import BaseModel
from typing import Dict, Any, Optional

class TransactionRequest(BaseModel):
    """
    Input schema for one transaction prediction request.

    For now, we accept a flexible dictionary of features.
    Later, this can be replaced with a stricter schema.
    """

    transaction_id: Optional[str] = None
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