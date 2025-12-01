#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

#define SIZE 100000

void merge(int arr[], int left, int mid, int right)
{
    int i, j, k;
    int n1 = mid - left + 1;
    int n2 = right - mid;

    int *L = (int *)malloc(n1 * sizeof(int));
    int *R = (int *)malloc(n2 * sizeof(int));

    for (i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];

    i = 0;
    j = 0;
    k = left;

    while (i < n1 && j < n2)
        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];

    while (i < n1)
        arr[k++] = L[i++];

    while (j < n2)
        arr[k++] = R[j++];

    free(L);
    free(R);
}

void serialMergeSort(int arr[], int left, int right)
{
    if (left < right)
    {
        int mid = left + (right - left) / 2;
        serialMergeSort(arr, left, mid);
        serialMergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

void parallelMergeSort(int arr[], int left, int right, int depth)
{
    if (left < right)
    {
        int mid = left + (right - left) / 2;

        if (depth <= 4)
        {
#pragma omp parallel sections
            {
#pragma omp section
                parallelMergeSort(arr, left, mid, depth + 1);
#pragma omp section
                parallelMergeSort(arr, mid + 1, right, depth + 1);
            }
        }
        else
        {
            serialMergeSort(arr, left, mid);
            serialMergeSort(arr, mid + 1, right);
        }

        merge(arr, left, mid, right);
    }
}

int main()
{
    int *arr_serial = (int *)malloc(SIZE * sizeof(int));
    int *arr_parallel = (int *)malloc(SIZE * sizeof(int));

    for (int i = 0; i < SIZE; i++)
    {
        int val = rand() % 100000;
        arr_serial[i] = val;
        arr_parallel[i] = val;
    }

    clock_t start_serial = clock();
    serialMergeSort(arr_serial, 0, SIZE - 1);
    clock_t end_serial = clock();
    double time_serial = (double)(end_serial - start_serial) / CLOCKS_PER_SEC;

    clock_t start_parallel = clock();
    parallelMergeSort(arr_parallel, 0, SIZE - 1, 0);
    clock_t end_parallel = clock();
    double time_parallel = (double)(end_parallel - start_parallel) / CLOCKS_PER_SEC;

    printf("Serial Merge Sort Time   : %.3f seconds\n", time_serial);
    printf("Parallel Merge Sort Time : %.6f seconds\n", time_parallel);

    for (int i = 0; i < SIZE; i++)
    {
        if (arr_serial[i] != arr_parallel[i])
        {
            printf("Mismatch at index %d\n", i);
            break;
        }
    }

    free(arr_serial);
    free(arr_parallel);
    return 0;
}
