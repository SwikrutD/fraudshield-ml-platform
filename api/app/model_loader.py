import json
import joblib

from api.app.config import MODEL_PATH, FEATURES_PATH, METADATA_PATH


def load_model():
    """
    Load the trained XGBoost model from disk.
    """

    return joblib.load(MODEL_PATH)


def load_feature_list():
    """
    Load the exact feature order used during training.

    This is important because the API must send features to the model
    in the same order used during training.
    """

    with open(FEATURES_PATH, "r") as file:
        return json.load(file)


def load_metadata():
    """
    Load metadata such as threshold, metrics, and model configuration.
    """

    with open(METADATA_PATH, "r") as file:
        return json.load(file)