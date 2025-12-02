import subprocess
import time
import os
import sys
import matplotlib.pyplot as plt

# ================= CONFIGURATION =================
# Matrix sizes to benchmark
# (Start small to verify it works, then increase)
MATRIX_SIZES = [128, 256, 512, 1024]

# Threads for Parallel versions
NUM_THREADS = 4 

OUTPUT_IMAGE = "benchmark_results.png"
FILE_A = "matrix_a.txt"
FILE_B = "matrix_b.txt"

# Executable paths
EXECUTABLES = {
    "Sequential": "bin/seq",
    "Pthreads":   "bin/thread2",
    "OpenMP":     "bin/omp",
    "MPI":        "bin/mpi"
}

# ================= HELPER FUNCTIONS =================

def generate_matrices(size):
    """
    Uses the repository's own 'random_float_matrix.py' to generate data.
    This ensures the format (headers, delimiters) is exactly what the C code expects.
    """
    generator_script = "random_float_matrix.py"
    
    if not os.path.exists(generator_script):
        print(f"[!] Critical: {generator_script} not found in this folder.")
        print("    Please ensure you are inside the 'matrix_multiplication' folder.")
        sys.exit(1)

    # We use os.system because redirection (>) is easier with shell commands
    # Command: python3 random_float_matrix.py <rows> <cols> > filename
    cmd_a = f"{sys.executable} {generator_script} {size} {size} > {FILE_A}"
    cmd_b = f"{sys.executable} {generator_script} {size} {size} > {FILE_B}"
    
    exit_code_a = os.system(cmd_a)
    exit_code_b = os.system(cmd_b)
    
    if exit_code_a != 0 or exit_code_b != 0:
        print("[!] Error generating matrix files.")
        sys.exit(1)

def run_benchmark(command, args):
    """
    Runs the command and returns time. Captures stdout/stderr for debugging.
    """
    full_cmd = command.split() + args
    start_time = time.time()
    
    try:
        # We capture BOTH stdout and stderr now so we don't miss error messages
        result = subprocess.run(
            full_cmd, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"    [!] Failed running: {' '.join(full_cmd)}")
        print(f"    [DEBUG] Output: {e.stdout}")
        print(f"    [DEBUG] Error:  {e.stderr}")
        return None

    return time.time() - start_time

# ================= MAIN EXECUTION =================

def main():
    # 1. Compile
    print("[-] Compiling code...")
    try:
        subprocess.run(["make"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("[!] Make failed.")
        return

    results = {method: [] for method in EXECUTABLES}

    print(f"[-] Starting Benchmarks on sizes: {MATRIX_SIZES}")
    print(f"[-] Threads: {NUM_THREADS}\n")

    for size in MATRIX_SIZES:
        print(f"--- Benchmarking Size: {size}x{size} ---")
        
        # Generate valid input files using the repo's tool
        print(f"    Generating matrices...", end="", flush=True)
        generate_matrices(size)
        print(" Done.")

        for method, exe_path in EXECUTABLES.items():
            if not os.path.exists(exe_path) and method != "MPI":
                print(f"    [!] {exe_path} not found.")
                results[method].append(None)
                continue

            cmd = exe_path
            args = [FILE_A, FILE_B] # All programs take file A and file B

            # Specific setup
            if method == "OpenMP":
                os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
            
            elif method == "MPI":
                cmd = f"mpirun -np {NUM_THREADS} {exe_path}"
                # MPI takes the same args, just wrapped in mpirun

            # Run
            print(f"    Running {method}...", end="", flush=True)
            elapsed = run_benchmark(cmd, args)
            
            if elapsed is not None:
                print(f" Time: {elapsed:.4f}s")
                results[method].append(elapsed)
            else:
                results[method].append(0)

    # Cleanup
    if os.path.exists(FILE_A): os.remove(FILE_A)
    if os.path.exists(FILE_B): os.remove(FILE_B)

    # Plot
    print(f"\n[-] Generating plot: {OUTPUT_IMAGE}")
    plt.figure(figsize=(10, 6))
    for method, times in results.items():
        # Only plot valid data
        clean_times = [t if t is not None else 0 for t in times]
        if any(clean_times):
            plt.plot(MATRIX_SIZES, clean_times, marker='o', label=method)
    
    plt.title(f"Matrix Multiplication Benchmark")
    plt.xlabel("Matrix Size (N)")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)
    plt.savefig(OUTPUT_IMAGE)
    print("[-] Success! Check 'benchmark_results.png'")

if __name__ == "__main__":
    main()
