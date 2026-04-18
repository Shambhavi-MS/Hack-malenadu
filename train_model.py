import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

data = {
    "feature1": [1, 2, 3, 4, 5, 6],
    "feature2": [10, 20, 30, 40, 50, 60],
    "feature3": [5, 4, 3, 2, 1, 0],
    "label": ["SAFE", "SAFE", "ATTACK", "ATTACK", "SAFE", "ATTACK"]
}

df = pd.DataFrame(data)

X = df[["feature1", "feature2", "feature3"]]
y = df["label"]

le = LabelEncoder()
y_encoded = le.fit_transform(y)

model = RandomForestClassifier()
model.fit(X, y_encoded)

joblib.dump(model, "model.pkl")
joblib.dump(le, "label_encoder.pkl")

print("Model created successfully!")
