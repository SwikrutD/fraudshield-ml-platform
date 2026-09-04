from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from api.app.database import get_db
from api.app.db_models import Transaction, ModelRun, Prediction, FraudAlert
from api.app.schemas import TransactionRequest, PredictionResponse
from api.app.prediction_service import predict_fraud, metadata


app = FastAPI(
    title="FraudShield ML API",
    description="API for scoring financial transactions using a trained XGBoost fraud detection model.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "FraudShield ML API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


def get_or_create_model_run(db: Session) -> ModelRun:
    """
    Create or reuse the model metadata row.
    """

    model_version = metadata["model_name"]

    existing_model = (
        db.query(ModelRun)
        .filter(ModelRun.model_version == model_version)
        .first()
    )

    if existing_model:
        return existing_model

    metrics = metadata.get("metrics", {})

    model_run = ModelRun(
        model_name=metadata["model_name"],
        model_version=model_version,
        algorithm=metadata.get("algorithm"),
        selected_threshold=metadata.get("selected_threshold"),
        precision_score=metrics.get("precision"),
        recall_score=metrics.get("recall"),
        f1_score=metrics.get("f1_score"),
        roc_auc=metrics.get("roc_auc"),
        pr_auc=metrics.get("pr_auc"),
        false_positive_rate=metrics.get("false_positive_rate"),
        training_rows=metadata.get("training_rows"),
        validation_rows=metadata.get("validation_rows"),
        num_features=metadata.get("num_features")
    )

    db.add(model_run)
    db.commit()
    db.refresh(model_run)

    return model_run


@app.post("/predict", response_model=PredictionResponse)
def predict_transaction(
    request: TransactionRequest,
    db: Session = Depends(get_db)
):
    """
    Score one transaction, return fraud risk, and log the result.
    """

    prediction_result = predict_fraud(request.features)

    model_run = get_or_create_model_run(db)

    transaction_amount = request.features.get("TransactionAmt")

    existing_transaction = (
    db.query(Transaction)
    .filter(Transaction.external_transaction_id == request.transaction_id)
    .first()
    )

    if existing_transaction:
        transaction = existing_transaction
    else:
        transaction = Transaction(
            external_transaction_id=request.transaction_id,
            amount=transaction_amount,
            is_fraud=request.actual_is_fraud
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    prediction = Prediction(
        transaction_id=transaction.transaction_id,
        model_run_id=model_run.model_run_id,
        fraud_probability=prediction_result["fraud_probability"],
        predicted_fraud=prediction_result["predicted_fraud"],
        decision_threshold=prediction_result["threshold"],
        risk_level=prediction_result["risk_level"],
        inference_time_ms=prediction_result["inference_time_ms"]
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    if prediction_result["predicted_fraud"]:
        alert = FraudAlert(
            transaction_id=transaction.transaction_id,
            prediction_id=prediction.prediction_id,
            risk_level=prediction_result["risk_level"],
            alert_status="new"
        )

        db.add(alert)
        db.commit()

    return {
        "transaction_id": request.transaction_id,
        "fraud_probability": prediction_result["fraud_probability"],
        "predicted_fraud": prediction_result["predicted_fraud"],
        "threshold": prediction_result["threshold"],
        "risk_level": prediction_result["risk_level"],
        "inference_time_ms": prediction_result["inference_time_ms"],
        "logged_to_database": True
    }