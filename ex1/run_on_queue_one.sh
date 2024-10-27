#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_GOL_one

## Output and error files
#PBS -o run_GOL_one.out
#PBS -e run_GOL_one.err

## How many machines should we get?
#PBS -l nodes=1:ppn=8

#PBS -l walltime=00:10:00

## Start
## Run make in the src folder (modify properly)

cd /home/parallel/parlab13

num_threads=8

printf "\n"
printf "Number of Threads used = $num_threads\n"
export OMP_NUM_THREADS=$num_threads
./Game_Of_Life 1024 1000
printf "\n"

