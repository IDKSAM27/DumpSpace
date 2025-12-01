#include<stdio.h>
#include<omp.h>

int main() {
	int n = 16, thread;
	
	printf("\nEnter the number of tasks:");
	scanf("%d", &n);

	printf("\nEnter the number of threads:");
	scanf("%d", &thread);

	omp_set_num_threads(thread);

	printf("\n-------------------\n");

#pragma omp parallel for schedule(static, 2)
	for (int i = 0; i < n; i++) {
		printf("Thread %d executes iteration %d\n", omp_get_thread_num(), i);
	}

	printf("--------------------\n");

	return 0;
}

// gcc -fopenmp lab2.c -o lab2
// ./lab2
