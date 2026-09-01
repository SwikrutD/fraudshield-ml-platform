from fastapi import FastAPI

from api.app.schemas import TransactionRequest, PredictionResponse
from api.app.prediction_service import predict_fraud


app = FastAPI(
    title="FraudShield ML API",
    description="API for scoring financial transactions using a trained XGBoost fraud detection model.",
    version="1.0.0"
)


@app.get("/")
def root():
    """
    Health check route.
    """

    return {
        "message": "FraudShield ML API is running"
    }


@app.get("/health")
def health_check():
    """
    Simple health check endpoint for deployment monitoring.
    """

    return {
        "status": "healthy"
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_transaction(request: TransactionRequest):
    """
    Score one transaction and return fraud risk.
    """

    prediction = predict_fraud(request.features)

    return {
        "transaction_id": request.transaction_id,
        "fraud_probability": prediction["fraud_probability"],
        "predicted_fraud": prediction["predicted_fraud"],
        "threshold": prediction["threshold"],
        "risk_level": prediction["risk_level"]
    }