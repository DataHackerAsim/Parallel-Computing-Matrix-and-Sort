CC = gcc
MPICC = mpic++
CFLAGS = -O3 -Wall -fopenmp
LIBS = -lm

# --- Targets ---
all: matrix sort

# Matrix Multiplication (Original Repo Files)
matrix: bin/seq bin/omp bin/thread2 bin/mpi

bin/seq: src/sequential.c
	$(CC) $(CFLAGS) -o bin/seq src/matrix.c src/sequential.c $(LIBS)

bin/omp: src/omp.c
	$(CC) $(CFLAGS) -o bin/omp src/matrix.c src/omp.c $(LIBS)

bin/thread2: src/thread2.c
	$(CC) $(CFLAGS) -pthread -o bin/thread2 src/matrix.c src/thread2.c $(LIBS)

bin/mpi: src/mpi.c
	$(MPICC) $(CFLAGS) -o bin/mpi src/matrix.c src/mpi.c $(LIBS)

# Sorting Algorithms (New Files)
sort: bin/sort_seq bin/sort_omp bin/sort_pthread

bin/sort_seq: sort_seq.c
	$(CC) $(CFLAGS) -o bin/sort_seq sort_seq.c

bin/sort_omp: sort_omp.c
	$(CC) $(CFLAGS) -o bin/sort_omp sort_omp.c

bin/sort_pthread: sort_pthread.c
	$(CC) $(CFLAGS) -pthread -o bin/sort_pthread sort_pthread.c

clean:
	rm -f bin/seq bin/omp bin/thread2 bin/mpi bin/sort_seq bin/sort_omp bin/sort_pthread
