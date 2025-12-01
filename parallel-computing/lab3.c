#include <stdio.h>
#include <omp.h>
#include <time.h>

int ser_fib(long int n)
{
    if (n < 2) return n;
    long int x, y;
    x = ser_fib(n - 1);
    y = ser_fib(n - 2);
    return x + y;
}

int fib(long int n)
{
    if (n < 2) return n;
    long int x, y;
#pragma omp task shared(x)
    x = fib(n - 1);
#pragma omp task shared(y)
    y = fib(n - 2);
#pragma omp taskwait
    return x + y;
}

int main()
{
    long int n = 10, result;
    clock_t start, end;
    double cpu_time;

    printf("\nEnter the value of n: ");
    scanf("%ld", &n);

    // Parallel Fibonacci
    start = clock();
#pragma omp parallel
    {
#pragma omp single
        result = fib(n);
    }
    end = clock();
    cpu_time = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Fibonacci(%ld) = %ld\n", n, result);
    printf("Time used in parallel mode = %f seconds\n", cpu_time);

    start = clock();
    result = ser_fib(n);
    end = clock();
    cpu_time = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Fibonacci(%ld) = %ld\n", n, result);
    printf("Time used in sequential mode = %f seconds\n", cpu_time);

    return 0;
}

// gcc -fopenmp lab3.c -o lab3
// ./lab3
