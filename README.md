# Parallel Computing Benchmark Suite

**Author:** Asim Ahmed  
**Department:** School of Interdisciplinary Engineering & Sciences (SINES)  
**Institution:** National University of Sciences and Technology (NUST)  
**Course:** Operating Systems (CS-313) | Class of 2027

---

## Project Overview
This project provides a comprehensive performance analysis of parallel computing paradigms. It benchmarks the execution efficiency of **Matrix Multiplication** and **Merge Sort** algorithms across distinct parallel architectures versus standard sequential processing.

The goal is to evaluate speedup, efficiency, and overhead on multi-core systems using **Shared Memory** (Pthreads, OpenMP) and **Distributed Memory** (MPI) models.

## Algorithms & Implementations

### Part 1: Matrix Multiplication
We benchmark the operation $C = A \times B$ across the following implementations:
* **Sequential:** Baseline single-core execution.
* **OpenMP:** Loop-level parallelism using `#pragma omp parallel for`.
* **MPI:** Process-level parallelism using Message Passing Interface (Scatter/Gather topology).
* **Pthreads:** Explicit multi-threading with partitioned workload.

**Test Sizes ($N \times N$):** $10, 500, 14000, 25000, 50000$

### Part 2: Sorting Algorithm (Merge Sort)
We compare the sorting performance of integer arrays using:
* **Sequential Merge Sort:** Standard recursive implementation.
* **OpenMP Merge Sort:** Task-based parallelism (`#pragma omp task`).
* **Pthreads Merge Sort:** Thread-based divide and conquer.

**Test Sizes (Elements):** $1k, 50k, 100k, 1M$

---

## Technical Requirements
To replicate this benchmark, your system requires:
* **OS:** Linux (Ubuntu/WSL recommended)
* **Compiler:** GCC with `build-essential`
* **MPI:** MPICH or OpenMPI (`sudo apt install mpich`)
* **Python:** Python 3.x with `matplotlib` for visualization

---

## How to Run

### 1. Compilation
A comprehensive `Makefile` is provided to build all executables (Matrix and Sorting versions).
```bash
make
