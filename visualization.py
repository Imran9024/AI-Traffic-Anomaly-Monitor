import matplotlib.pyplot as plt
import os

def plot_anomalies(df, output_path="visualizations/anomalies.png"):
    """
    Generate a scatter plot highlighting anomalies.
    Expects df to have 'byte_size', 'packet_count', and 'is_anomaly' columns.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    # Normal traffic
    normal = df[df['is_anomaly'] == False]
    plt.scatter(normal['packet_count'], normal['byte_size'], c='blue', label='Normal', alpha=0.6)
    
    # Anomalous traffic
    anomalies = df[df['is_anomaly'] == True]
    plt.scatter(anomalies['packet_count'], anomalies['byte_size'], c='red', label='Anomaly', marker='x', s=100)
    
    plt.xlabel('Packet Count')
    plt.ylabel('Byte Size')
    plt.title('Network Traffic Anomalies Detection')
    plt.legend()
    plt.grid(True)
    
    plt.savefig(output_path)
    plt.close()
