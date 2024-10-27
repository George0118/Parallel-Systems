import matplotlib.pyplot as plt

# Read data from the file
with open('new_config_extracted_info.txt', 'r') as file:
    data = file.readlines()

# Initialize dictionaries to store time data for each category and block size
naive_data = {}
transpose_data = {}
shared_data = {}
sequential_data = None

# Parse data and fill dictionaries
for line in data:
    parts = line.split(', ')
    title = parts[0]
    total_time = float(parts[1].split(': ')[1].split(' ms')[0])

    # Extract block size if available, otherwise set it to 0
    block_size = int(parts[2].split(': ')[1]) if 'Block Size' in line else 0

    if 'Naive' in title:
        naive_data[str(block_size)] = total_time
    elif 'Transpose' in title:
        transpose_data[str(block_size)] = total_time
    elif 'Shared' in title:
        shared_data[str(block_size)] = total_time
    elif 'Sequential' in title:
        sequential_data = total_time

# Extract block sizes and corresponding times for each category
naive_block_sizes, naive_times = zip(*sorted(naive_data.items(), key=lambda x: int(x[0])))
transpose_block_sizes, transpose_times = zip(*sorted(transpose_data.items(), key=lambda x: int(x[0])))
shared_block_sizes, shared_times = zip(*sorted(shared_data.items(), key=lambda x: int(x[0])))

# Plotting for Naive
plt.figure(figsize=(10, 6))
plt.bar(naive_block_sizes, naive_times, width=0.3, color='blue')
plt.xlabel('Block Size')
plt.ylabel('Total Time (ms)')
plt.yscale('log')
plt.title('Naive GPU Kmeans Total Time for Different Block Sizes')
plt.show()

# Plotting for Transpose
plt.figure(figsize=(10, 6))
plt.bar(transpose_block_sizes, transpose_times, width=0.3, color='green')
plt.xlabel('Block Size')
plt.ylabel('Total Time (ms)')
plt.yscale('log')
plt.title('Transpose GPU Kmeans Total Time for Different Block Sizes')
plt.show()

# Plotting for Shared
plt.figure(figsize=(10, 6))
plt.bar(shared_block_sizes, shared_times, width=0.3, color='red')
plt.xlabel('Block Size')
plt.ylabel('Total Time (ms)')
plt.yscale('log')
plt.title('Shared GPU Kmeans Total Time for Different Block Sizes')
plt.show()

# Calculate ratios for Sequential time to each algorithm's time
naive_ratios = [sequential_data / time for time in naive_times]
transpose_ratios = [sequential_data / time for time in transpose_times]
shared_ratios = [sequential_data / time for time in shared_times]

# Plotting for Naive Ratio
plt.figure(figsize=(10, 6))
plt.bar(naive_block_sizes, naive_ratios, width=0.3, color='blue')
plt.xlabel('Block Size')
plt.ylabel('Sequential Time / Naive Time Ratio')
plt.yscale('log')
plt.title('Sequential Time / Naive GPU Kmeans Time Ratio for Different Block Sizes')
plt.show()

# Plotting for Transpose Ratio
plt.figure(figsize=(10, 6))
plt.bar(transpose_block_sizes, transpose_ratios, width=0.3, color='green')
plt.xlabel('Block Size')
plt.ylabel('Sequential Time / Transpose Time Ratio')
plt.yscale('log')
plt.title('Sequential Time / Transpose GPU Kmeans Time Ratio for Different Block Sizes')
plt.show()

# Plotting for Shared Ratio
plt.figure(figsize=(10, 6))
plt.bar(shared_block_sizes, shared_ratios, width=0.3, color='red')
plt.xlabel('Block Size')
plt.ylabel('Sequential Time / Shared Time Ratio')
plt.yscale('log')
plt.title('Sequential Time / Shared GPU Kmeans Time Ratio for Different Block Sizes')
plt.show()
