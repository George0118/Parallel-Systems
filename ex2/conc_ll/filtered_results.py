import re

def extract_information(log_file):
    with open(log_file, 'r') as file:
        lines = file.readlines()

    data = []
    current_type = None
    current_nthreads = None
    current_throughput = None
    current_workload = None

    for line in lines:
        match_parameters = re.match(r"Parameters: (\d+),", line)
        match_type = re.match(r'(Serial|Coarse-grain locking|Fine-grain locking|Optimistic Synchronization|Lazy Synchronization|Non-blocking Synchronization)', line)
        match_info = re.match(r"Nthreads: (\d+)  .*? Workload: (\d+/\d+/\d+) .*? Throughput\(Kops\/sec\):\s*([\d.]+)", line)

        if match_parameters:
            current_size = match_parameters.group(1)
        if match_type:
            current_type = match_type.group(1)
        elif match_info:
            current_nthreads = int(match_info.group(1))
            current_workload = match_info.group(2)
            current_throughput = float(match_info.group(3))
            data.append((current_size, current_type, current_nthreads, current_throughput, current_workload))
            # Reset current state after adding the information
            current_type = None
            current_nthreads = None
            current_throughput = None
            current_workload = None

    return data

def save_to_file(data, file_name='filtered_data.txt'):
    with open(file_name, 'w') as file:
        for entry in data:
            file.write(f"{entry}\n")

log_file = './run_conc_ll.txt'
extracted_data = extract_information(log_file)

# Save the extracted data to a file
save_to_file(extracted_data)
