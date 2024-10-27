import re

def extract_info(log):
    # Extract Title
    title_match = re.search(r'\|[-]+(.*?)[-]+\|', log)
    title = title_match.group(1).strip() if title_match else None

    # Extract total time
    total_time_match = re.search(r'total = (.*? )ms', log)
    total_time = float(total_time_match.group(1).strip()) if total_time_match else None

    # Extract block size
    block_size_match = re.search(r'block_size = (\d+)', log)
    block_size = int(block_size_match.group(1)) if block_size_match else None

    # Extract GPU Time
    gpu_time_match = re.search(r'GPU Time: (.*?)\n', log)
    gpu_time = float(gpu_time_match.group(1).strip()) if gpu_time_match else None

    # Extract CPU - GPU Transfers
    cpu_gpu_transfers_match = re.search(r'CPU - GPU Transfers: (.*?)\n', log)
    cpu_gpu_transfers = float(cpu_gpu_transfers_match.group(1).strip()) if cpu_gpu_transfers_match else None

    # Extract CPU Time
    cpu_time_match = re.search(r'CPU Time: (.*?)\n', log)
    cpu_time = float(cpu_time_match.group(1).strip()) if cpu_time_match else None

    return title, total_time, block_size, gpu_time, cpu_gpu_transfers, cpu_time

# Read logs from "timed_results.txt" file
file_path = "new_config_results.txt"
with open(file_path, 'r') as file:
    logs = file.read()

# Split logs into individual sections
log_sections = re.split(r'~+', logs)

# Write extracted information to "timed_extracted_info.txt" file
output_file_path = "new_config_extracted_info.txt"
with open(output_file_path, 'w') as output_file:
    # Process each log section
    for log_section in log_sections:
        title, total_time, block_size, gpu_time, cpu_gpu_transfers, cpu_time = extract_info(log_section)
        if title is not None and total_time is not None:
            output_file.write(f"Title: {title}, Total Time: {total_time} ms")
            if block_size is not None:
                output_file.write(f", Block Size: {block_size}")
            if gpu_time is not None:
                output_file.write(f", GPU Time: {gpu_time} ms")
            if cpu_gpu_transfers is not None:
                output_file.write(f", CPU - GPU Transfers: {cpu_gpu_transfers} ms")
            if cpu_time is not None:
                output_file.write(f", CPU Time: {cpu_time} ms")
            output_file.write("\n")

print(f"Extracted information written to {output_file_path}")
