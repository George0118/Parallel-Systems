def extract_information(log_file):
    with open(log_file, 'r') as file:
        lines = file.readlines()

    relevant_lines = []

    for line in lines:
        if line.startswith('OpenMP Kmeans'):
            relevant_lines.append(line.strip())
        elif line.startswith('        nloops ='):
            relevant_lines.append(line.strip())

    return relevant_lines

log_file = './run_kmeans.txt'
relevant_info = extract_information(log_file)

output_file = 'filtered_results.txt'

with open(output_file, 'w') as output:
    for line in relevant_info:
        output.write(line + '\n')

print(f"Filtered results have been written to {output_file}")

