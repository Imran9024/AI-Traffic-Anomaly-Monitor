import numpy as np
from sklearn.ensemble import IsolationForest

def train_model(data):
    model = IsolationForest(contamination=0.1)
    model.fit(data)
    return model

def predict(model, data):
    return model.predict(data)
