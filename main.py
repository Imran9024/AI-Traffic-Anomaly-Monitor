import argparse
import os
import subprocess
from src.preprocessing import load_data, preprocess_data
from src.model import train_model
from src.detection import detect_anomalies
from src.model_utils import save_model, load_model, save_scaler, load_scaler
from src.sniffing import start_sniffing
from src.visualization import plot_anomalies

def main():
    parser = argparse.ArgumentParser(description="Anomaly-Based Network Traffic Monitoring System")
    parser.add_argument('--train', action='store_true', help='Train the Isolation Forest model')
    parser.add_argument('--predict', action='store_true', help='Predict anomalies on sample data')
    parser.add_argument('--sniff', action='store_true', help='Capture live network packets and predict')
    parser.add_argument('--dashboard', action='store_true', help='Launch Flask dashboard')
    
    args = parser.parse_args()
    
    if args.train:
        print("[*] Loading sample data for training...")
        data = load_data("data/sample_data.csv")
        print("[*] Preprocessing data...")
        X, scaler = preprocess_data(data)
        
        print("[*] Training model...")
        model = train_model(X)
        
        print("[*] Saving model and scaler...")
        save_model(model, "models/isolation_forest.pkl")
        save_scaler(scaler, "models/scaler.pkl")
        print("[+] Training complete!")
        
    elif args.predict:
        print("[*] Loading data for prediction...")
        data = load_data("data/sample_data.csv")
        
        model = load_model("models/isolation_forest.pkl")
        scaler = load_scaler("models/scaler.pkl")
        
        if model is None or scaler is None:
            print("[!] Model not found! Please run with --train first.")
            return
            
        X, _ = preprocess_data(data, scaler=scaler)
        results = detect_anomalies(model, X)
        
        # Merge original data with anomaly columns
        final_df = data.copy()
        final_df['is_anomaly'] = results['is_anomaly']
        
        # Save to results.csv for dashboard
        os.makedirs("data", exist_ok=True)
        final_df.to_csv("data/results.csv", index=False)
        print("[+] Predictions saved to data/results.csv")
        
        print("[*] Generating visualizations...")
        os.makedirs("static/visualizations", exist_ok=True)
        plot_anomalies(final_df, "static/visualizations/anomalies.png")
        print("[+] Visualizations saved to static/visualizations/anomalies.png")
        
        print(final_df.head(10))
        
    elif args.sniff:
        print("[*] Starting packet sniffer...")
        data = start_sniffing(timeout=15)
        
        if data.empty:
            print("[-] No packets captured.")
            return
            
        model = load_model("models/isolation_forest.pkl")
        scaler = load_scaler("models/scaler.pkl")
        
        if model is None or scaler is None:
            print("[!] Model not found! Please run with --train first.")
            return
            
        print("[*] Predicting anomalies on live traffic...")
        X, _ = preprocess_data(data, scaler=scaler)
        results = detect_anomalies(model, X)
        
        final_df = data.copy()
        final_df['is_anomaly'] = results['is_anomaly']
        
        # Save for dashboard
        os.makedirs("data", exist_ok=True)
        final_df.to_csv("data/results.csv", index=False)
        print("[+] Live capture saved to data/results.csv")
        
        os.makedirs("static/visualizations", exist_ok=True)
        plot_anomalies(final_df, "static/visualizations/anomalies.png")
        print(final_df)

    elif args.dashboard:
        print("[*] Launching Web Dashboard...")
        subprocess.run(["python", "app.py"])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
