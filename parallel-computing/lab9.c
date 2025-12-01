// reduce_allreduce_mpi.c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv)
{
  int rank, value, sum, max;
  MPI_Init(&argc, &argv); // Initialize MPI
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  value = rank + 1; // Each process gets a value
// Reduce to find the sum at rank 0
  MPI_Reduce(&value, &sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
  if (rank == 0)
    printf("Sum using Reduce: %d\n", sum);
// Allreduce to find the max across all processes
  MPI_Allreduce(&value, &max, 1, MPI_INT, MPI_MAX, MPI_COMM_WORLD);
  printf("Max using Allreduce (rank %d): %d\n", rank, max);
  MPI_Finalize();

  return 0;
}

// mpicc lab9.c -o lab9
// mpirun -np 4 ./lab9
