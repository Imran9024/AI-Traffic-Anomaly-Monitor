import joblib
import os

def save_model(model, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)

def load_model(filepath):
    if os.path.exists(filepath):
        return joblib.load(filepath)
    return None

def save_scaler(scaler, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(scaler, filepath)

def load_scaler(filepath):
    if os.path.exists(filepath):
        return joblib.load(filepath)
    return None
