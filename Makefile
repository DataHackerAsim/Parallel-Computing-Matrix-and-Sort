# Compiler settings
CC = g++
MPICC = mpic++
CFLAGS = -O3 -Wall
OMP_FLAGS = -fopenmp
PTHREAD_FLAGS = -pthread

# Targets
all: serial pthread openmp mpi

serial: serial.c
	$(CC) $(CFLAGS) -o serial serial.c

pthread: parallel_pthread.c
	$(CC) $(CFLAGS) $(PTHREAD_FLAGS) -o pthread parallel_pthread.c

openmp: parallel_omp.c
	$(CC) $(CFLAGS) $(OMP_FLAGS) -o openmp parallel_omp.c

mpi: parallel_mpi.c
	$(MPICC) $(CFLAGS) -o mpi parallel_mpi.c

clean:
	rm -f serial pthread openmp mpi
