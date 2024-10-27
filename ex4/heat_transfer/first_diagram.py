import matplotlib.pyplot as plt
import numpy as np
import os

def read_data(file_path, gsize):
    with open(file_path, 'r') as file:
        data = file.read()

    lines = data.strip().split('\n')
    processes_count = 1
    num_proc = []
    speedups = []
    reference_total_time = None

    for i, line in enumerate(lines):
        parts = line.split()
        size = parts[2] + " x " + parts[4]  # Calculate the size as X * Y
        total_time = float(parts[parts.index("TotalTime") + 1])

        if reference_total_time is None and size == gsize:
            reference_total_time = total_time
        
        if(size == gsize):
            speedup = reference_total_time / total_time
            num_proc.append(str(processes_count))
            speedups.append(speedup)

        if (i + 1) % 3 == 0:
            processes_count *= 2

    return num_proc, speedups

def plot_speedup_for_method(method_name, num_proc, speedups):
    plt.plot(num_proc, speedups, marker='o', label=f'{method_name} Speedup')

def plot_speedup_for_size_for_all_methods(tuples, size):
    plt.figure()

    for file_path, method in tuples:
        num_proc, speedups = read_data(file_path, size)
        plot_speedup_for_method(method, num_proc, speedups)

    plt.xlabel('Number of MPI Processes')
    plt.ylabel('Speedup')
    plt.title(f'Speedup vs Number of MPI Processes for Size: {size}')
    plt.legend()

    # Set y-axis limits to include zero
    plt.ylim(bottom=0)

    plt.show()

# Specify the file paths for all methods
gssor_path = 'GSSOR_results.txt'
jac_path = 'JAC_results.txt'
rbsor_path = 'RBSOR_results.txt'

# Plot for GaussSeidelSOR
plot_speedup_for_size_for_all_methods([(gssor_path, "GaussSeidelSOR"), (jac_path, "Jacobi"), (rbsor_path, "RedBlackSOR")], '2048 x 2048')

# Plot for Jacobi
plot_speedup_for_size_for_all_methods([(gssor_path, "GaussSeidelSOR"), (jac_path, "Jacobi"), (rbsor_path, "RedBlackSOR")], '4096 x 4096')

# Plot for RedBlackSOR
plot_speedup_for_size_for_all_methods([(gssor_path, "GaussSeidelSOR"), (jac_path, "Jacobi"), (rbsor_path, "RedBlackSOR")], '6144 x 6144')
