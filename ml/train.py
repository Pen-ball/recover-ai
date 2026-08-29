import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix
)
from xgboost import XGBClassifier
import joblib


NUMERIC_FEATURES = [
    "amount", "retry_count", "total_transactions",
    "successful_transactions", "failed_transactions",
    "average_transaction_value", "lifetime_value",
    "historical_success_rate",
]


def load_and_prepare_data():
    transactions = pd.read_csv("simulator/data/synthetic_transactions.csv")
    customers = pd.read_csv("simulator/data/synthetic_customers.csv")

    df = transactions.merge(
        customers[[
            "customer_id", "total_transactions", "successful_transactions",
            "failed_transactions", "average_transaction_value", "lifetime_value"
        ]],
        on="customer_id",
        how="left",
        suffixes=("", "_customer")
    )

    return df


def build_features(df):
    df["historical_success_rate"] = (
        df["successful_transactions"] / df["total_transactions"].replace(0, 1)
    )

    df_encoded = pd.get_dummies(
        df,
        columns=["failure_reason", "payment_method"],
        drop_first=False
    )

    feature_columns = NUMERIC_FEATURES + [
        col for col in df_encoded.columns
        if col.startswith("failure_reason_") or col.startswith("payment_method_")
    ]

    X = df_encoded[feature_columns]
    y = df_encoded["recovered"]

    return X, y, feature_columns


def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "precision": round(precision_score(y_test, y_pred), 3),
        "recall": round(recall_score(y_test, y_pred), 3),
        "f1": round(f1_score(y_test, y_pred), 3),
        "roc_auc": round(roc_auc_score(y_test, y_prob), 3),
    }

    print(f"--- {name} ---")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print()

    return metrics


if __name__ == "__main__":
    df = load_and_prepare_data()
    X, y, feature_columns = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Training set size:", X_train.shape[0])
    print("Test set size:", X_test.shape[0])
    print()

    # --- Logistic Regression (scaled) ---
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[NUMERIC_FEATURES] = scaler.fit_transform(X_train[NUMERIC_FEATURES])
    X_test_scaled[NUMERIC_FEATURES] = scaler.transform(X_test[NUMERIC_FEATURES])

    log_reg = LogisticRegression(max_iter=1000)
    log_reg.fit(X_train_scaled, y_train)
    log_reg_metrics = evaluate_model("Logistic Regression", log_reg, X_test_scaled, y_test)

    # --- XGBoost ---
    # Tree-based models do NOT need feature scaling - they split on raw
    # thresholds (e.g. "amount > 5000"), so scale doesn't affect them.
    xgb_model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        eval_metric="logloss",
        random_state=42,
    )
    xgb_model.fit(X_train, y_train)
    xgb_metrics = evaluate_model("XGBoost", xgb_model, X_test, y_test)

    # --- Decide which model to keep as the "production" model ---
    # We select based on ROC-AUC, since it best reflects overall
    # ranking quality for a probability-based decision system like ours.
    if xgb_metrics["roc_auc"] >= log_reg_metrics["roc_auc"]:
        print("Selected model: XGBoost (higher ROC-AUC)")
        best_model = xgb_model
        best_model_name = "xgboost"
    else:
        print("Selected model: Logistic Regression (higher ROC-AUC)")
        best_model = log_reg
        best_model_name = "logistic_regression"

    joblib.dump(best_model, f"ml/models/{best_model_name}.pkl")
    joblib.dump(scaler, "ml/models/scaler.pkl")
    joblib.dump(feature_columns, "ml/models/feature_columns.pkl")

    # Save which model type was selected, so the backend knows how to load it
    joblib.dump(best_model_name, "ml/models/selected_model_type.pkl")

    print(f"Saved best model as ml/models/{best_model_name}.pkl")

