import pandas as pd

def load_data(file):
    return pd.read_csv(file)

def preprocess(df):
    return df.select_dtypes(include=['int64', 'float64'])
