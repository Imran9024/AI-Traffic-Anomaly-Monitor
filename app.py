import streamlit as st
import pandas as pd
from src.model import train_model, predict
from src.utils import load_data, preprocess

st.set_page_config(page_title="AI Traffic Monitor", layout="wide")

st.title("🚀 AI Traffic Anomaly Monitor")

uploaded_file = st.file_uploader("Upload Traffic Dataset", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    st.write("### Raw Data", df.head())

    data = preprocess(df)

    model = train_model(data)
    result = predict(model, data)

    df['Anomaly'] = result

    st.write("### 📊 Processed Data", df.head())

    st.line_chart(data)

    anomalies = df[df['Anomaly'] == -1]

    if not anomalies.empty:
        st.error("🚨 Anomalies Detected!")
        st.write(anomalies)
    else:
        st.success("✅ No Anomalies Found")
