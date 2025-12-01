// scatter_gather_mpi.c
#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv)
{
  int rank, size;
  int send_data[4] = {10, 20, 30, 40};
  int recv_data;
// Initialize MPI
  MPI_Init(&argc, &argv);
// Get rank and size
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
// Scatter: send one element to each process
  MPI_Scatter(send_data, 1, MPI_INT, &recv_data, 1, MPI_INT, 0, MPI_COMM_WORLD);
  printf("Process %d received: %d\n", rank, recv_data);
// Each process increments the received value
  recv_data += 1;
// Gather: collect updated values back to root process
  MPI_Gather(&recv_data, 1, MPI_INT, send_data, 1, MPI_INT, 0, MPI_COMM_WORLD);
// Root prints gathered data
  if (rank == 0)
  {
    printf("Gathered data: ");
    for (int i = 0; i < size; i++)
      printf("%d ", send_data[i]);
    printf("\n");
  }
  MPI_Finalize();
  return 0;
}
