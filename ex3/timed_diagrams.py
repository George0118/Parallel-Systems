import matplotlib.pyplot as plt
import numpy as np  

def extract_data(file_path):
    naive_data = {'Block Size': [], 'Total Time': [], 'GPU Time': [], 'CPU Time': [], 'CPU - GPU Transfers': []}
    transpose_data = {'Block Size': [], 'Total Time': [], 'GPU Time': [], 'CPU Time': [], 'CPU - GPU Transfers': []}
    shared_data = {'Block Size': [], 'Total Time': [], 'GPU Time': [], 'CPU Time': [], 'CPU - GPU Transfers': []}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith('Title: Naive GPU Kmeans'):
            tokens = line.split(', ')
            block_size = int(tokens[2].split(': ')[1])
            total_time = float(tokens[1].split(': ')[1].replace(' ms', ''))
            gpu_time = float(tokens[3].split(': ')[1].replace(' ms', ''))
            cpu_gpu_transfers = float(tokens[4].split(': ')[1].replace(' ms', ''))
            cpu_time = float(tokens[5].split(': ')[1].replace(' ms', ''))

            naive_data['Block Size'].append(str(block_size))
            naive_data['Total Time'].append(total_time)
            naive_data['GPU Time'].append(gpu_time)
            naive_data['CPU - GPU Transfers'].append(cpu_gpu_transfers)
            naive_data['CPU Time'].append(cpu_time)
        elif line.startswith('Title: Transpose GPU Kmeans'):
            tokens = line.split(', ')
            block_size = int(tokens[2].split(': ')[1])
            total_time = float(tokens[1].split(': ')[1].replace(' ms', ''))
            gpu_time = float(tokens[3].split(': ')[1].replace(' ms', ''))
            cpu_gpu_transfers = float(tokens[4].split(': ')[1].replace(' ms', ''))
            cpu_time = float(tokens[5].split(': ')[1].replace(' ms', ''))

            transpose_data['Block Size'].append(str(block_size))
            transpose_data['Total Time'].append(total_time)
            transpose_data['GPU Time'].append(gpu_time)
            transpose_data['CPU - GPU Transfers'].append(cpu_gpu_transfers)
            transpose_data['CPU Time'].append(cpu_time)
        elif line.startswith('Title: Shared GPU Kmeans'):
            tokens = line.split(', ')
            block_size = int(tokens[2].split(': ')[1])
            total_time = float(tokens[1].split(': ')[1].replace(' ms', ''))
            gpu_time = float(tokens[3].split(': ')[1].replace(' ms', ''))
            cpu_gpu_transfers = float(tokens[4].split(': ')[1].replace(' ms', ''))
            cpu_time = float(tokens[5].split(': ')[1].replace(' ms', ''))

            shared_data['Block Size'].append(str(block_size))
            shared_data['Total Time'].append(total_time)
            shared_data['GPU Time'].append(gpu_time)
            shared_data['CPU - GPU Transfers'].append(cpu_gpu_transfers)
            shared_data['CPU Time'].append(cpu_time)
        elif line.startswith('Title:'):
            current_data = None
            continue

    return naive_data, transpose_data, shared_data

def plot_bar(data, title):
    block_size = data['Block Size']
    total_time = data['Total Time']
    gpu_time = np.array(data['GPU Time']) / np.array(total_time) * 100
    cpu_gpu_transfers = np.array(data['CPU - GPU Transfers']) / np.array(total_time) * 100
    cpu_time = np.array(data['CPU Time']) / np.array(total_time) * 100
    total_time = np.array(total_time) / np.array(total_time) * 100

    fig, ax = plt.subplots()

    X_axis = np.arange(len(block_size))

    ax.bar(X_axis - 0.2, total_time, label='Total Time', width=0.2, color='b')
    ax.bar(X_axis + 0.2, gpu_time, label='GPU Time', width=0.2, color='g')
    ax.bar(X_axis + 0.2, cpu_gpu_transfers, label='CPU - GPU Transfers', width=0.2, bottom=gpu_time, color='r')
    ax.bar(X_axis + 0.2, cpu_time, label='CPU Time', width=0.2, bottom=[i + j for i, j in zip(gpu_time, cpu_gpu_transfers)], color='orange')

    plt.xticks(X_axis, block_size)
    ax.set_xlabel('Block Size')
    ax.set_ylabel('Percentage of Total Time')
    ax.set_title(title)

    # Add annotations
    for i, v in enumerate(total_time):
        ax.text(i - 0.2, v - 50, f'{v:.2f}', color='black', ha='center', va='bottom')

    for i, v in enumerate(gpu_time):
        ax.text(i + 0.2, v - 15, f'{v:.2f}', color='black', ha='center', va='bottom')

    for i, v in enumerate(cpu_gpu_transfers):
        ax.text(i + 0.2, v + gpu_time[i] - 3, f'{v:.2f}', color='black', ha='center', va='bottom')

    for i, v in enumerate(cpu_time):
        ax.text(i + 0.2, v + gpu_time[i] + cpu_gpu_transfers[i] - 40, f'{v:.2f}', color='black', ha='center', va='bottom')

    ax.legend()
    plt.show()

if __name__ == "__main__":
    file_path = 'new_config_extracted_info.txt'
    naive_data, transpose_data, shared_data = extract_data(file_path)

    plot_bar(naive_data, 'Naive GPU Kmeans')
    plot_bar(transpose_data, 'Transpose GPU Kmeans')
    plot_bar(shared_data, 'Shared GPU Kmeans')
