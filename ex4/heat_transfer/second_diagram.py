import matplotlib.pyplot as plt
import numpy as np
import os

def read_data(file_path, gsize, proc):
    with open(file_path, 'r') as file:
        data = file.read()

    lines = data.strip().split('\n')
    processes_count = 1
    total_times = []
    communication_times = []
    computation_times = []

    for i, line in enumerate(lines):
        parts = line.split()
        size = parts[2] + " x " + parts[4]  # Calculate the size as X * Y
        total_time = float(parts[parts.index("TotalTime") + 1])
        communication_time = float(parts[parts.index("CommunicationTime") + 1])
        computation_time = float(parts[parts.index("ComputationTime") + 1])
        
        if(size == gsize and processes_count == proc):
            total_times.append(total_time)
            communication_times.append(communication_time)
            computation_times.append(computation_time)

        if (i + 1) % 3 == 0:
            processes_count *= 2

    return total_times, communication_times, computation_times


def plot_analysis_for_size_for_all_methods(tuples, size):
    for proc in [8, 16, 32, 64]:  
        total_times = []
        communication_times = []
        computation_times = []  
        methods = []
        for file_path, method in tuples:
            
            total_time, communication_time, computation_time = read_data(file_path, size, proc)

            methods.append(method)
            total_times.append(total_time[0])
            communication_times.append(communication_time[0])
            computation_times.append(computation_time[0])

        # Plot two bars for each method
        bar_width = 0.35  # Width of the bars
        index = np.arange(len(methods))  # The label locations

        plt.figure()
        plt.bar(index, total_times, bar_width, color='blue', label='TotalTime')
        plt.bar(index + bar_width, computation_times, bar_width, color='green', label='ComputationTime')
        #plt.bar(index + bar_width, communication_times, bar_width, color='red', label='CommunicationTime', bottom=computation_times)

        plt.xlabel('Methods')
        plt.ylabel('Time (s)')
        plt.title(f'Times For each Method: {size} - {proc} MPI Processes')
        plt.xticks(index + bar_width / 2, methods)
        plt.legend()
        plt.show()

# Specify the file paths for all methods
gssor_path = 'GSSOR_results.txt'
jac_path = 'JAC_results.txt'
rbsor_path = 'RBSOR_results.txt'

# Plot analysis for GaussSeidelSOR
plot_analysis_for_size_for_all_methods([(gssor_path, "GaussSeidelSOR"), (jac_path, "Jacobi"), (rbsor_path, "RedBlackSOR")], '2048 x 2048')

# Plot analysis for Jacobi
plot_analysis_for_size_for_all_methods([(gssor_path, "GaussSeidelSOR"), (jac_path, "Jacobi"), (rbsor_path, "RedBlackSOR")], '4096 x 4096')

# Plot analysis for RedBlackSOR
plot_analysis_for_size_for_all_methods([(gssor_path, "GaussSeidelSOR"), (jac_path, "Jacobi"), (rbsor_path, "RedBlackSOR")], '6144 x 6144')
