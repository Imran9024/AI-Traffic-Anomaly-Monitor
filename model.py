from sklearn.ensemble import IsolationForest

def train_model(X):
    model = IsolationForest(contamination=0.2)
    model.fit(X)
    return model
