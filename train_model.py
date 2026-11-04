"""Train a baseline AQI-category classifier from the Kaggle India air-quality CSV."""
import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import StandardScaler

DATA = "data/air_quality.csv"
OUT = "models"
FEATURES = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
TARGET = "AQI_Bucket"

def main():
    if not os.path.exists(DATA):
        raise SystemExit(f"Dataset not found: {DATA}. Download the Kaggle CSV and save it there.")
    df = pd.read_csv(DATA)
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise SystemExit("Missing required columns: " + ", ".join(missing))
    data = df[FEATURES + [TARGET]].copy()
    for c in FEATURES:
        data[c] = pd.to_numeric(data[c], errors="coerce")
    data[TARGET] = data[TARGET].astype("string").str.strip()
    data = data.dropna(subset=[TARGET])
    data = data[data[TARGET] != ""]
    X, y = data[FEATURES], data[TARGET]
    if y.nunique() < 2:
        raise SystemExit("Need at least two AQI_Bucket classes to train a classifier.")
    stratify = y if y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=stratify
    )
    pre = Pipeline([("imputer", SimpleImputer(strategy="median"))])
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced"))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    metrics = {
        "test_rows": int(len(y_test)),
        "accuracy": float(accuracy_score(y_test, pred)),
        "macro_f1": float(f1_score(y_test, pred, average="macro")),
        "classification_report": classification_report(y_test, pred, output_dict=True, zero_division=0),
        "features": FEATURES,
        "target": TARGET,
        "random_state": 42
    }
    os.makedirs(OUT, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES, "target": TARGET}, f"{OUT}/aqi_bucket_model.joblib")
    with open(f"{OUT}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print(json.dumps({k:v for k,v in metrics.items() if k != "classification_report"}, indent=2))
    print(f"Saved model to {OUT}/aqi_bucket_model.joblib and metrics to {OUT}/metrics.json")

if __name__ == "__main__":
    main()
