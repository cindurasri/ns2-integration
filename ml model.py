import pandas as pd
import matplotlib.pyplot as plt

# Load trace data from NS2
def load_trace_data(file_path):
    trace_data = pd.read_csv(file_path, delim_whitespace=True, header=None)
    return trace_data

# Function to calculate performance metrics
def calculate_metrics(trace_data):
    # Extract the necessary information from the trace
    sent_packets = trace_data[trace_data[1] == 's'].shape[0]
    received_packets = trace_data[trace_data[1] == 'r'].shape[0]
    total_time = trace_data[trace_data[0] == 'r'][0].max()  # Time at which last packet is received
    
    # Calculate PDR
    pdr = (received_packets / sent_packets) * 100 if sent_packets > 0 else 0
    
    # Calculate end-to-end delay
    delays = trace_data[trace_data[1] == 'r'][0] - trace_data[trace_data[1] == 's'][0]
    average_delay = delays.mean() if not delays.empty else 0

    # Calculate throughput
    throughput = (sent_packets * 1000 * 8) / total_time  # Kbps
    
    return average_delay, pdr, throughput

# Load model predictions
predictions = pd.read_csv('predictions.csv')  # Your predictions file

# Store results
results = {
    'num_nodes': [],
    'end_to_end_delay': [],
    'pdr': [],
    'throughput': []
}

# Evaluate for different node configurations
for num_nodes in [20, 50, 100]:
    trace_file = f'out_{num_nodes}.tr'  # Assuming trace files are named accordingly
    trace_data = load_trace_data(trace_file)
    
    # Calculate metrics
    delay, pdr, throughput = calculate_metrics(trace_data)
    
    # Append results
    results['num_nodes'].append(num_nodes)
    results['end_to_end_delay'].append(delay)
    results['pdr'].append(pdr)
    results['throughput'].append(throughput)

# Create a DataFrame for visualization
results_df = pd.DataFrame(results)

# Plotting results
plt.figure(figsize=(15, 5))

# Plot End-to-End Delay
plt.subplot(1, 3, 1)
plt.bar(results_df['num_nodes'], results_df['end_to_end_delay'])
plt.title('End-to-End Delay')
plt.xlabel('Number of Nodes')
plt.ylabel('Delay (seconds)')

# Plot Packet Delivery Ratio
plt.subplot(1, 3, 2)
plt.bar(results_df['num_nodes'], results_df['pdr'])
plt.title('Packet Delivery Ratio (PDR)')
plt.xlabel('Number of Nodes')
plt.ylabel('PDR (%)')

# Plot Throughput
plt.subplot(1, 3, 3)
plt.bar(results_df['num_nodes'], results_df['throughput'])
plt.title('Throughput')
plt.xlabel('Number of Nodes')
plt.ylabel('Throughput (Kbps)')

plt.tight_layout()
plt.show()
