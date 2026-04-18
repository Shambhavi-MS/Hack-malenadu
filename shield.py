import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import datetime

# Configuration
DATA_PATH = "data/network_data.csv"
MODEL_PATH = "models/shield_model.pkl"
FEATURES = ['duration', 'src_bytes', 'dst_bytes', 'num_connections', 'error_rate']

# Load data
def load_data(path):
    print("📂 Loading data...")
    df = pd.read_csv(path)

    X = df[FEATURES]
    y = df['label']

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X, y_encoded, le

# Train model
def train_model(X, y):
    print("🤖 Training model...")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Balanced model (not too strong)
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))

    return model

# Save model
def save_model(model):
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("💾 Model saved successfully!")

# Predict
def predict(model, le, traffic_row):
    df = pd.DataFrame([traffic_row])
    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]

    label = le.inverse_transform([prediction])[0]
    confidence = max(probabilities)

    return {
        "label": label,
        "confidence": f"{confidence*100:.1f}%",
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
        "raw": traffic_row
    }

# MAIN
if __name__ == "__main__":
    X, y, le = load_data(DATA_PATH)
    model = train_model(X, y)
    save_model(model)

    # Test sample
    test_traffic = {
        'duration': 5,
        'src_bytes': 9999,
        'dst_bytes': 0,
        'num_connections': 499,
        'error_rate': 0.95
    }

    result = predict(model, le, test_traffic)
    print(f"\n🧪 Test Result: {result['label']} ({result['confidence']} confidence)")
