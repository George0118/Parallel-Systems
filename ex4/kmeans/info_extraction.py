import re

def extract_info(line, mpi_processes):
    match = re.search(r'nloops\s*=\s*(\d+)\s+\(total\s*=\s*(\d+\.\d+)s\s*\)\s*\(per loop\s*=\s*(\d+\.\d+)s\s*\)', line)
    if match:
        nloops, total_time, per_loop_time = match.groups()
        return f"MPI processes={mpi_processes}, total time={total_time}s"
    else:
        return None

def main():
    with open('results.txt', 'r') as file:
        lines = file.readlines()

    with open('extracted_info.txt', 'w') as output_file:
        mpi_processes = 1
        for line in lines:
            info = extract_info(line, mpi_processes)
            if info:
                mpi_processes *= 2
                output_file.write(f"{info}\n")

if __name__ == "__main__":
    main()
