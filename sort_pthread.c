#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct Params { int *arr; int l; int r; };

void merge(int *arr, int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;
    int *L = (int*)malloc(n1 * sizeof(int));
    int *R = (int*)malloc(n2 * sizeof(int));
    for (i = 0; i < n1; i++) L[i] = arr[l + i];
    for (j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
    i = 0; j = 0; k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
    free(L); free(R);
}

void *mergeSortThread(void *arg) {
    struct Params *p = (struct Params*)arg;
    int l = p->l; int r = p->r; int *arr = p->arr;
    
    if (l < r) {
        int m = l + (r - l) / 2;
        // Only create threads if array is large enough, else distinct
        if (r - l > 10000) {
            struct Params p1 = {arr, l, m};
            struct Params p2 = {arr, m + 1, r};
            pthread_t t1, t2;
            pthread_create(&t1, NULL, mergeSortThread, &p1);
            pthread_create(&t2, NULL, mergeSortThread, &p2);
            pthread_join(t1, NULL);
            pthread_join(t2, NULL);
        } else {
            // Sequential fallback for small chunks
             struct Params p1 = {arr, l, m};
             struct Params p2 = {arr, m + 1, r};
             mergeSortThread(&p1);
             mergeSortThread(&p2);
        }
        merge(arr, l, m, r);
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    int n = atoi(argv[1]);
    int *arr = (int*)malloc(n * sizeof(int));
    for(int i=0; i<n; i++) arr[i] = rand() % 1000;

    struct Params p = {arr, 0, n - 1};
    mergeSortThread(&p);
    
    free(arr);
    return 0;
}
