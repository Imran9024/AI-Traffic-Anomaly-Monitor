import pandas as pd

def detect_anomalies(model, X):
    preds = model.predict(X)
    df = pd.DataFrame(X)
    # IsolationForest outputs 1 for normal, -1 for anomaly
    df['anomaly'] = preds
    df['is_anomaly'] = df['anomaly'].apply(lambda x: True if x == -1 else False)
    return df
