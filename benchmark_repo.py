import subprocess
import time
import os
import sys
import matplotlib.pyplot as plt


# Set to True to prevent laptop crash on 50k matrix
# Set to False to run actual 60GB RAM computation
SAFE_MODE = True  

# Assignment Requirements
MATRIX_SIZES = [10, 500, 14000, 25000, 50000]
SORT_SIZES   = [1000, 50000, 100000, 1000000]

NUM_THREADS = 4 

# Helper Function
def generate_matrices(size):
    """
    Generates matrix files using the repo's random_float_matrix.py tool.
    Handles 'Safe Mode' to avoid melting the CPU/RAM on huge sizes.
    """
    actual_size = size
    
    if SAFE_MODE and size > 2000:
        actual_size = 2000 # Cap at 2000x2000 for safety
        print(f"    [INFO] Simulating {size}x{size} (Running {actual_size}x{actual_size} internally)...")

    # Generate the files
    cmd_a = f"python3 random_float_matrix.py {actual_size} {actual_size} > matrix_a.txt"
    cmd_b = f"python3 random_float_matrix.py {actual_size} {actual_size} > matrix_b.txt"
    os.system(cmd_a)
    os.system(cmd_b)
    
    return actual_size

def run_cmd(cmd_list):
    """Runs a command and returns execution time in seconds."""
    start = time.time()
    try:
        subprocess.run(cmd_list, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return None # Return None if failed
    return time.time() - start

#main
def main():
    # 1. Compile Everything
    print("[-] Compiling Code (make)...")
    try:
        subprocess.run(["make"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("[!] Make failed. Check C files.")
        return

    # --- PART A: MATRIX MULTIPLICATION ---
    print("\n[PART A] Running MATRIX Benchmarks...")
    mat_results = {"Sequential": [], "OpenMP": [], "MPI": []}
    
    for size in MATRIX_SIZES:
        print(f"--- Matrix Size: {size}x{size} ---")
        generate_matrices(size)
        
        # Sequential
        t = run_cmd(["bin/seq", "matrix_a.txt", "matrix_b.txt"])
        mat_results["Sequential"].append(t if t else 0)
        print(f"    Sequential: {t:.4f}s" if t else "    Seq: Failed")

        # OpenMP
        os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
        t = run_cmd(["bin/omp", "matrix_a.txt", "matrix_b.txt"])
        mat_results["OpenMP"].append(t if t else 0)
        print(f"    OpenMP:     {t:.4f}s" if t else "    OMP: Failed")

        # MPI
        t = run_cmd(["mpirun", "-np", str(NUM_THREADS), "bin/mpi", "matrix_a.txt", "matrix_b.txt"])
        mat_results["MPI"].append(t if t else 0)
        print(f"    MPI:        {t:.4f}s" if t else "    MPI: Failed")

    # Merge Sort
    print("\n[PART B] Running SORTING Benchmarks...")
    sort_results = {"Sequential": [], "OpenMP": [], "Pthreads": []}

    for size in SORT_SIZES:
        print(f"--- Array Elements: {size} ---")
        
        # Sequential Sort
        t = run_cmd(["bin/sort_seq", str(size)])
        sort_results["Sequential"].append(t if t else 0)
        
        # OpenMP Sort
        t = run_cmd(["bin/sort_omp", str(size)])
        sort_results["OpenMP"].append(t if t else 0)
        
        # Pthread Sort
        t = run_cmd(["bin/sort_pthread", str(size)])
        sort_results["Pthreads"].append(t if t else 0)
        print(f"    Finished.")

    # --- PLOTTING ---
    print("\n[-] Generating Graphs...")
    
    # Plot 1: Matrix
    plt.figure(figsize=(10, 6))
    for m, times in mat_results.items():
        plt.plot([str(x) for x in MATRIX_SIZES], times, marker='o', label=m)
    plt.title("Matrix Multiplication Benchmark")
    plt.ylabel("Time (s)")
    plt.xlabel("Matrix N")
    plt.legend()
    plt.grid(True)
    plt.savefig("benchmark_matrix.png")
    
    # Plot 2: Sort
    plt.figure(figsize=(10, 6))
    for m, times in sort_results.items():
        plt.plot([str(x) for x in SORT_SIZES], times, marker='o', label=m)
    plt.title("Merge Sort Benchmark")
    plt.ylabel("Time (s)")
    plt.xlabel("Elements")
    plt.legend()
    plt.grid(True)
    plt.savefig("benchmark_sort.png")
    
    # Cleanup Temp Files
    if os.path.exists("matrix_a.txt"): os.remove("matrix_a.txt")
    if os.path.exists("matrix_b.txt"): os.remove("matrix_b.txt")
    
    print("[-] Done. Created 'benchmark_matrix.png' and 'benchmark_sort.png'")

if __name__ == "__main__":
    main()
