import requests
import pandas as pd
import streamlit as st


# Base URL for the FastAPI backend.
# Later, when Docker is added, this can come from an environment variable.
API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="FraudShield Dashboard",
    page_icon="🛡️",
    layout="wide"
)


st.title("FraudShield ML Platform")
st.caption("Real-time fraud scoring, prediction logging, and alert monitoring")


def fetch_api_data(endpoint: str):
    """
    Helper function to call a FastAPI endpoint.

    Example:
    fetch_api_data("/metrics") calls:
    http://127.0.0.1:8000/metrics
    """

    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        st.error(f"Could not fetch data from {endpoint}: {error}")
        return None


# -----------------------------
# Dashboard metrics
# -----------------------------

metrics = fetch_api_data("/metrics")

if metrics:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Predictions",
        metrics["total_predictions"]
    )

    col2.metric(
        "Total Alerts",
        metrics["total_alerts"]
    )

    col3.metric(
        "Predicted Fraud",
        metrics["predicted_fraud_count"]
    )

    col4.metric(
        "Avg Fraud Probability",
        f"{metrics['average_fraud_probability']:.2%}"
    )

    st.divider()

    risk_col1, risk_col2, risk_col3 = st.columns(3)

    risk_col1.metric(
        "Critical Alerts",
        metrics["critical_alerts"]
    )

    risk_col2.metric(
        "High Alerts",
        metrics["high_alerts"]
    )

    risk_col3.metric(
        "Medium Alerts",
        metrics["medium_alerts"]
    )

else:
    st.warning("Metrics are unavailable. Make sure the FastAPI server is running.")


# -----------------------------
# Recent predictions
# -----------------------------

st.subheader("Recent Predictions")

predictions = fetch_api_data("/predictions?limit=50")

if predictions:
    predictions_df = pd.DataFrame(predictions)

    st.dataframe(
        predictions_df,
        use_container_width=True,
        hide_index=True
    )

    if "risk_level" in predictions_df.columns:
        st.subheader("Prediction Risk-Level Breakdown")

        risk_counts = (
            predictions_df["risk_level"]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = ["risk_level", "count"]

        st.bar_chart(
            risk_counts,
            x="risk_level",
            y="count"
        )

else:
    st.info("No prediction records found yet. Run POST /predict first.")


# -----------------------------
# Fraud alerts
# -----------------------------

st.subheader("Fraud Alerts")

alerts = fetch_api_data("/alerts?limit=50")

if alerts:
    alerts_df = pd.DataFrame(alerts)

    st.dataframe(
        alerts_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No fraud alerts found yet. This is normal if recent predictions were low risk.")