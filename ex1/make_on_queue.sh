#!/bin/bash

## Give the Job a descriptive name
#PBS -N make_GOL

## Output and error files
#PBS -o make_GOL.out
#PBS -e make_GOL.err

## How many machines should we get?
#PBS -l nodes=1:ppn=2

#PBS -l walltime=00:10:00

## Start 
## Run make in the src folder (modify properly)

cd /home/parallel/parlab13
make


