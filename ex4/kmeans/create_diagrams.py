import matplotlib.pyplot as plt

# Read data from the file
with open("extracted_info.txt", "r") as file:
    lines = file.readlines()

# Parse data
data = []
for line in lines:
    parts = line.strip().split(', ')
    mpi_processes = parts[0].split('=')[1]
    total_time = float(parts[1].split('=')[1][:-1])  # Removing the 's' at the end
    data.append({"MPI_processes": mpi_processes, "total_time": total_time})

# Extracting relevant information
mpi_processes = [entry["MPI_processes"] for entry in data]
total_times = [entry["total_time"] for entry in data]

# Calculate speedup compared to the first process
speedup = [total_times[0] / time for time in total_times]

# Replace "1" with "1 (Sequential)"
mpi_processes = ["1 (Sequential)" if process == "1" else process for process in mpi_processes]

# Bar plot of total times with values on top
plt.figure(figsize=(10, 5))
bars = plt.bar(mpi_processes, total_times, width=0.4, color='blue')
plt.title('Total Time vs MPI Processes for Kmeans Algorithm')
plt.xlabel('MPI Processes')
plt.ylabel('Total Time (s)')

# Add values on top of each bar
for bar, time in zip(bars, total_times):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{time:.4f}', ha='center', va='bottom')

plt.show()

# Bar plot of speedup with values on top
plt.figure(figsize=(10, 5))
bars = plt.bar(mpi_processes, speedup, width=0.4, color='green')  # Exclude the first process for speedup
plt.title('Speedup of MPI Implementation compared to Sequential for Kmeans Algorithm')
plt.xlabel('MPI Processes')
plt.ylabel('Speedup')

# Add values on top of each bar
for bar, spd in zip(bars, speedup):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{spd:.4f}', ha='center', va='bottom')

plt.show()
