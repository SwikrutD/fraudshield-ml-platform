import pandas as pd

from api.app.model_loader import load_model, load_feature_list, load_metadata


# Load model artifacts once when this module is imported.
# This is better than loading the model on every request.
model = load_model()
feature_list = load_feature_list()
metadata = load_metadata()

# Use the selected threshold saved during model artifact creation.
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

    The model expects:
    - same columns used during training
    - same column order
    - numeric values
    """

    # Create one-row DataFrame from incoming request
    input_df = pd.DataFrame([input_features])

    # Add any missing model features with value 0
    # This prevents prediction errors if the request does not include every feature.
    for feature in feature_list:
        if feature not in input_df.columns:
            input_df[feature] = 0

    # Keep only model features in the correct order
    input_df = input_df[feature_list]

    # Convert all values to numeric where possible
    input_df = input_df.apply(pd.to_numeric, errors="coerce")

    # Fill any invalid/missing numeric values with 0
    input_df = input_df.fillna(0)

    return input_df


def predict_fraud(input_features: dict) -> dict:
    """
    Generate a fraud prediction from input transaction features.
    """

    model_input = prepare_features(input_features)

    fraud_probability = model.predict_proba(model_input)[:, 1][0]

    predicted_fraud = fraud_probability >= selected_threshold

    risk_level = assign_risk_level(fraud_probability)

    return {
        "fraud_probability": float(fraud_probability),
        "predicted_fraud": bool(predicted_fraud),
        "threshold": float(selected_threshold),
        "risk_level": risk_level
    }