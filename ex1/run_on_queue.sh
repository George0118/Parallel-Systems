#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_GOL

## Output and error files
#PBS -o run_GOL.out
#PBS -e run_GOL.err

## How many machines should we get?
#PBS -l nodes=1:ppn=8

#PBS -l walltime=00:10:00

## Start
## Run make in the src folder (modify properly)

cd /home/parallel/parlab13

for num_threads in 1 2 4 6 8
do
    printf "\n"
    printf "Number of Threads used = $num_threads\n"
    export OMP_NUM_THREADS=$num_threads
    ./Game_Of_Life 64 1000
    ./Game_Of_Life 1024 1000
    ./Game_Of_Life 4096 1000
    printf "\n"
done
