import re
import matplotlib.pyplot as plt

def extract_information(log_file):
    with open(log_file, 'r') as file:
        lines = file.readlines()

    data = []
    current_kmeans_type = None
    current_num_threads = None
    current_total_time = None

    for line in lines:
        match_kmeans = re.match(r'OpenMP Kmeans - (.+?)\s*\(number of threads: (\d+)\)', line)
        match_nloops = re.match(r'nloops =  \d+\s+\(total =\s+(\d+\.\d+)s\)\s+\(per loop =  (\d+\.\d+)s\)', line)

        print(match_kmeans)
        print(match_nloops)

        if match_kmeans:
            current_kmeans_type = match_kmeans.group(1)
            current_num_threads = int(match_kmeans.group(2))
        elif match_nloops:
            current_total_time = float(match_nloops.group(1))
            data.append((current_kmeans_type, current_num_threads, current_total_time))
            # Reset current state after adding the information
            current_kmeans_type = None
            current_num_threads = None
            current_total_time = None

    return data

log_file = './filtered_results.txt'
extracted_data = extract_information(log_file)

# Separate data by Kmeans type
kmeans_types = list(set(entry[0] for entry in extracted_data))

# Define the specific thread numbers you want on the x-axis
specific_threads = [1, 2, 4, 8, 16, 32, 64]

# Plotting
plt.figure(figsize=(12, 6))

for kmeans_type in kmeans_types:
    threads = [entry[1] for entry in extracted_data if entry[0] == kmeans_type and entry[1] in specific_threads]
    times = [entry[2] for entry in extracted_data if entry[0] == kmeans_type and entry[1] in specific_threads]
    plt.plot(threads, times, marker='o', label=f'{kmeans_type}')

plt.xlabel('Number of Threads')
plt.ylabel('Total Time (s)')
plt.title('OpenMP Kmeans Performance')
plt.legend()
plt.grid(True)

# Set specific thread numbers on the x-axis with equal distances (log scale)
plt.xscale('log', base=2)
plt.xticks(specific_threads, [str(thread) for thread in specific_threads])

plt.show()