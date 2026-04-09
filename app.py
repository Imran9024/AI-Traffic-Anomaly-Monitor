from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Load recent predictions if they exist
    results_path = "data/results.csv"
    if os.path.exists(results_path):
        df = pd.read_csv(results_path)
        total_packets = len(df)
        anomaly_count = len(df[df['is_anomaly'] == True])
        normal_count = len(df[df['is_anomaly'] == False])
        
        # Get the most recent 10 records
        recent_data = df.tail(10).to_dict('records')
    else:
        total_packets = 0
        anomaly_count = 0
        normal_count = 0
        recent_data = []

    # Check if visualization exists
    image_exists = os.path.exists("static/visualizations/anomalies.png")

    return render_template('index.html',
                           total_packets=total_packets,
                           normal_count=normal_count,
                           anomaly_count=anomaly_count,
                           recent_data=recent_data,
                           image_exists=image_exists)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
