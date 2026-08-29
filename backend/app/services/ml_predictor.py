import joblib
import pandas as pd

_model = None
_scaler = None
_feature_columns = None

NUMERIC_FEATURES = [
    "amount", "retry_count", "total_transactions",
    "successful_transactions", "failed_transactions",
    "average_transaction_value", "lifetime_value",
    "historical_success_rate",
]


def _load_artifacts():
    global _model, _scaler, _feature_columns
    if _model is None:
        _model = joblib.load("ml/models/logistic_regression.pkl")
        _scaler = joblib.load("ml/models/scaler.pkl")
        _feature_columns = joblib.load("ml/models/feature_columns.pkl")
    return _model, _scaler, _feature_columns


def predict_recovery_probability(transaction_row: dict) -> float:
    model, scaler, feature_columns = _load_artifacts()

    row = dict(transaction_row)
    row["historical_success_rate"] = (
        row["successful_transactions"] / max(row["total_transactions"], 1)
    )

    df = pd.DataFrame([row])
    df_encoded = pd.get_dummies(df, columns=["failure_reason", "payment_method"])

    for col in feature_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    df_encoded = df_encoded[feature_columns]

    df_encoded[NUMERIC_FEATURES] = scaler.transform(df_encoded[NUMERIC_FEATURES])

    probability = model.predict_proba(df_encoded)[0][1]
    return float(probability)
