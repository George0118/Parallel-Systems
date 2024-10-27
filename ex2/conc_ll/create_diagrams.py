import matplotlib.pyplot as plt
import re

# Define the specific thread numbers you want on the x-axis
specific_threads = [1, 2, 4, 8, 16, 32, 64, 128]

# Function to parse the line and extract relevant information
def parse_line(line):
    match = re.match(r"\('(\d+)', '([^']+)', (\d+), ([\d.]+), '([^']+)'\)", line)
    if match:
        size, type, threads, throughput, workload = match.groups()
        return int(size), type, int(threads), float(throughput), workload
    return None

# Function to generate diagrams
def generate_diagrams(file_path):
    # Dictionary to store data for each size, workload, and type
    data_dict = {}

    with open(file_path, 'r') as file:
        for line in file:
            parsed_data = parse_line(line)
            if parsed_data:
                size, type, threads, throughput, workload = parsed_data

                # Create a unique identifier for each size and workload
                identifier = (size, workload)

                # Initialize or append data to the dictionary
                if identifier not in data_dict:
                    data_dict[identifier] = {'types': [], 'threads': [], 'throughput': []}
                data_dict[identifier]['types'].append(type)
                data_dict[identifier]['threads'].append(threads)
                data_dict[identifier]['throughput'].append(throughput)

    # Generate diagrams for each size and workload
    for identifier, data in data_dict.items():
        size, workload = identifier

        plt.figure()
        for type in set(data['types']):
            # Filter data for the specific type
            type_data = [data['throughput'][i] for i in range(len(data['types'])) if data['types'][i] == type]
            type_threads = [data['threads'][i] for i in range(len(data['types'])) if data['types'][i] == type]

            # Extend Serial values to all threads
            if type == "Serial":
                serial_value = type_data[0]
                type_data = [serial_value] * len(specific_threads)
                type_threads = specific_threads

            plt.plot(type_threads, type_data, marker='o', label=type)

        plt.title(f'Throughput vs Threads - Size: {size}, Workload: {workload}')
        plt.xlabel('Threads')
        plt.xscale('log', base=2)
        plt.xticks(specific_threads, [str(thread) for thread in specific_threads])
        plt.ylabel('Throughput')
        plt.legend()
        plt.grid(True)
        plt.show()

# Example usage
generate_diagrams('filtered_data.txt')
