import requests
import pandas as pd


# API endpoint running locally through Uvicorn
API_URL = "http://127.0.0.1:8000/predict"

# Load the same feature-engineered dataset used by the model
data = pd.read_parquet(
    "data/processed/train_transaction_features.parquet",
    engine="fastparquet"
)

# Match the same validation split used during model training
split_index = int(len(data) * 0.8)
validation_data = data.iloc[split_index:].copy()

# Pick one validation transaction to test
sample_row = validation_data.loc[0]

# Save true label separately so we can compare after prediction
actual_is_fraud = int(sample_row["isFraud"])

# Remove columns that the API/model should not receive as features
features = sample_row.drop(labels=["isFraud", "TransactionID"]).to_dict()

# Create request body for FastAPI
payload = {
    "transaction_id": str(sample_row["TransactionID"]),
    "features": features
}

# Send POST request to the local API
response = requests.post(API_URL, json=payload)

# Show response status and prediction
print("Status code:", response.status_code)
print("API response:")
print(response.json())

print("Actual isFraud:", actual_is_fraud)