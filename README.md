# High-Performance Matrix Multiplication Benchmark

**Author:** Asim Ahmed  
**Course:** Operating Systems
**Institution:** NUST (Class of 2027)
**Department:** School of Interdisciplinary Engineering and Sciences

## Overview
This project benchmarks the performance of Matrix Multiplication using four different methods. It compares sequential execution against various parallel computing techniques.

**Methods Implemented:**
1.  **Sequential:** Baseline single-core implementation.
2.  **Pthreads:** Multi-threading using POSIX threads.
3.  **OpenMP:** Parallelization using compiler directives.
4.  **MPI:** Distributed computing using Message Passing Interface.

## Prerequisites
To run this project, ensure the following are installed on your system:
* GCC Compiler (build-essential)
* MPICH (for MPI)
* Python 3
* Matplotlib Library (`pip install matplotlib`)

## How to Run
Follow these steps to reproduce the benchmark results:

1.  **Compile the Code**
    Run the makefile to build all executables:
    ```bash
    make
    ```

2.  **Run the Benchmark Suite**
    Execute the Python script to generate data, run tests, and plot results:
    ```bash
    python3 benchmark_repo.py
    ```

3.  **View Results**
    The script generates a performance graph named `benchmark_results.png`.

## Project Structure
* `src/`: Contains C source code for all implementations.
* `bin/`: Stores the compiled executable files.
* `benchmark_repo.py`: Automation script for testing and plotting.
* `random_float_matrix.py`: Helper script for generating matrix data.
* `Makefile`: Build configuration file.
