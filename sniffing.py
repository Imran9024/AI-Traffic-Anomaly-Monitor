from scapy.all import sniff, IP, TCP, UDP
import time
import pandas as pd

# Global dict to store ongoing flows temporarily
# Key: (src_ip, dst_ip, protocol), Value: {'start_time': t, 'byte_size': b, 'packet_count': c}
flows = {}

def packet_callback(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet[IP].proto
        
        flow_key = (src_ip, dst_ip, protocol)
        packet_len = len(packet)
        curr_time = time.time()
        
        if flow_key not in flows:
            flows[flow_key] = {
                'start_time': curr_time,
                'byte_size': packet_len,
                'packet_count': 1
            }
        else:
            flows[flow_key]['byte_size'] += packet_len
            flows[flow_key]['packet_count'] += 1

def start_sniffing(interface=None, timeout=10):
    """
    Sniff packets for a given timeout and extract flows.
    """
    global flows
    flows = {} # Reset flows
    print(f"[*] Starting packet capture on interface {interface if interface else 'default'} for {timeout} seconds...")
    try:
        sniff(iface=interface, prn=packet_callback, store=0, timeout=timeout)
    except PermissionError:
        print("[!] Permission denied: You may need root privileges to capture packets.")
        return pd.DataFrame(columns=['packet_count', 'byte_size', 'duration'])

    data = []
    curr_time = time.time()
    for key, flow_data in flows.items():
        duration = curr_time - flow_data['start_time']
        if duration <= 0:
            duration = 0.01  # avoid zero division
        data.append({
            'packet_count': flow_data['packet_count'],
            'byte_size': flow_data['byte_size'],
            'duration': duration
        })
    
    df = pd.DataFrame(data)
    if df.empty:
        # Return empty DF with expected columns
        df = pd.DataFrame(columns=['packet_count', 'byte_size', 'duration'])
    return df
