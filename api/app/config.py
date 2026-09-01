from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Saved model folder
MODEL_DIR = PROJECT_ROOT / "models" / "fraud_xgboost_v1"

# Specific model artifact paths
MODEL_PATH = MODEL_DIR / "model.joblib"
FEATURES_PATH = MODEL_DIR / "features.json"
METADATA_PATH = MODEL_DIR / "metadata.json"