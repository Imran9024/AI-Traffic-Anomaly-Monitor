import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_data(path):
    return pd.read_csv(path)

def preprocess_data(data, scaler=None):
    if scaler is None:
        scaler = StandardScaler()
        X = scaler.fit_transform(data)
    else:
        X = scaler.transform(data)
    return X, scaler
