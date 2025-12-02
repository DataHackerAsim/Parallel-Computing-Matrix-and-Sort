import subprocess
import time
import matplotlib.pyplot as plt
import os
import sys

# ================= CONFIGURATION =================
# Matrix sizes to benchmark (N x N)
# Warning: large sizes (e.g., 2048+) will take very long for sequential code
MATRIX_SIZES = [128, 256, 512, 1024]

# Number of threads/processes for parallel execution
NUM_THREADS = 4 

# Executable names (must match Makefile output)
EXECUTABLES = {
    "Sequential": "./serial",
    "Pthreads": "./pthread",
    "OpenMP": "./openmp",
    "MPI": "./mpi"
}

# Store results: results[Method][Size] = Time
results = {method: [] for method in EXECUTABLES}

# ================= HELPER FUNCTIONS =================

def compile_code():
    """Runs the make command to build C/C++ files."""
    print("[-] Compiling code using Makefile...")
    try:
        subprocess.run(["make", "clean"], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["make"], check=True, stdout=subprocess.DEVNULL)
        print("[+] Compilation successful.\n")
    except subprocess.CalledProcessError:
        print("[!] Compilation failed. Check your C code or Makefile.")
        sys.exit(1)

def run_benchmark(command, input_size):
    """
    Runs a command and measures execution time.
    Passes input_size as a command line argument if the C program expects it.
    """
    start_time = time.time()
    
    try:
        # Construct the full command
        # Assuming the C programs accept size as the first argument: ./serial 512
        cmd_list = command.split() + [str(input_size)]
        
        # Execute
        subprocess.run(cmd_list, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        
    except subprocess.CalledProcessError as e:
        print(f"    [!] Error running {' '.join(cmd_list)}")
        return None

    end_time = time.time()
    return end_time - start_time

# ================= MAIN EXECUTION =================

def main():
    if not os.path.exists("Makefile"):
        print("[!] Makefile not found. Please create it first.")
        return

    # 1. Compile
    compile_code()

    # 2. Run Benchmarks
    print(f"[-] Starting Benchmarks on sizes: {MATRIX_SIZES}")
    print(f"[-] Using {NUM_THREADS} threads/processes for parallel versions.")

    for size in MATRIX_SIZES:
        print(f"\n--- Benchmarking Matrix Size: {size}x{size} ---")
        
        for method_name, exe_path in EXECUTABLES.items():
            
            # Setup specific environment or command adjustments
            final_cmd = exe_path
            
            if method_name == "Pthreads":
                # Pthreads usually takes thread count as arg or hardcoded
                # Assuming arg structure: ./pthread <size> <threads>
                final_cmd = f"{exe_path} {NUM_THREADS}" 
            
            elif method_name == "OpenMP":
                # OpenMP uses Environment Variable
                os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
                final_cmd = f"{exe_path}" # Size added in run_benchmark
            
            elif method_name == "MPI":
                # MPI requires mpirun wrapper
                final_cmd = f"mpirun -np {NUM_THREADS} {exe_path}"

            # If sequential, just the executable path is needed
            
            # Run and Measure
            print(f"    Running {method_name}...", end="", flush=True)
            elapsed = run_benchmark(final_cmd, size)
            
            if elapsed is not None:
                print(f" Done. Time: {elapsed:.4f}s")
                results[method_name].append(elapsed)
            else:
                results[method_name].append(0)

    # 3. Generate Plot
    print("\n[-] Generating Results Graph...")
    generate_plot()

def generate_plot():
    plt.figure(figsize=(10, 6))
    
    for method, times in results.items():
        if any(times): # Only plot if we have data
            plt.plot(MATRIX_SIZES, times, marker='o', label=method)

    plt.title(f'Matrix Multiplication Benchmark (Lower is Better)\nThreads/Processes: {NUM_THREADS}')
    plt.xlabel('Matrix Size (N)')
    plt.ylabel('Time (Seconds)')
    plt.grid(True, which="both", ls="-")
    plt.legend()
    
    output_file = 'benchmark_results.png'
    plt.savefig(output_file)
    print(f"[+] Plot saved as {output_file}")
    plt.show()

if __name__ == "__main__":
    main()
