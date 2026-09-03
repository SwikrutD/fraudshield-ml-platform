import time

import pandas as pd

from api.app.model_loader import load_model, load_feature_list, load_metadata


model = load_model()
feature_list = load_feature_list()
metadata = load_metadata()

selected_threshold = metadata["selected_threshold"]


def assign_risk_level(fraud_probability: float) -> str:
    """
    Convert fraud probability into a human-readable risk level.
    """

    if fraud_probability >= 0.90:
        return "critical"
    elif fraud_probability >= 0.70:
        return "high"
    elif fraud_probability >= selected_threshold:
        return "medium"
    else:
        return "low"


def prepare_features(input_features: dict) -> pd.DataFrame:
    """
    Convert request features into a model-ready DataFrame.
    """

    input_df = pd.DataFrame([input_features])

    for feature in feature_list:
        if feature not in input_df.columns:
            input_df[feature] = 0

    input_df = input_df[feature_list]
    input_df = input_df.apply(pd.to_numeric, errors="coerce")
    input_df = input_df.fillna(0)

    return input_df


def predict_fraud(input_features: dict) -> dict:
    """
    Generate fraud prediction and measure inference time.
    """

    model_input = prepare_features(input_features)

    start_time = time.perf_counter()

    fraud_probability = model.predict_proba(model_input)[:, 1][0]

    end_time = time.perf_counter()

    inference_time_ms = (end_time - start_time) * 1000

    predicted_fraud = fraud_probability >= selected_threshold
    risk_level = assign_risk_level(fraud_probability)

    return {
        "fraud_probability": float(fraud_probability),
        "predicted_fraud": bool(predicted_fraud),
        "threshold": float(selected_threshold),
        "risk_level": risk_level,
        "inference_time_ms": float(inference_time_ms)
    }