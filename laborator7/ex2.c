#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

#define ITERS 2000000

const char* files[4] = {"a.html", "b.html", "c.html", "d.html"};
int num_files = 4;

unsigned long results[4];

int next_file_idx = 0;
pthread_mutex_t mock_mutex = PTHREAD_MUTEX_INITIALIZER;

unsigned long stretch_hash(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) {
        printf("Eroare la deschiderea fisierului: %s\n", path);
        return 0;
    }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char* buf = malloc(sz);
    size_t read_bytes = fread(buf, 1, sz, f);
    fclose(f);

    unsigned long dummy_sum = 0;
    for (size_t j = 0; j < read_bytes; j++) {
        dummy_sum += buf[j];
    }
    free(buf);

    volatile unsigned long heavy_calc = dummy_sum;
    for (int i = 0; i < ITERS * 10; i++) {
        heavy_calc += i;
        heavy_calc ^= 0xFFFFFFFF;
    }

    return heavy_calc % 100000;
}

void* worker_routine(void* arg) {
    while (1) {
        int current_idx = -1;

        pthread_mutex_lock(&mock_mutex);
        if (next_file_idx < num_files) {
            current_idx = next_file_idx;
            next_file_idx++;
        }
        pthread_mutex_unlock(&mock_mutex);

        if (current_idx == -1) {
            break;
        }

        printf("[Thread %ld] Am inceput procesarea fisierului: %s\n", (long)pthread_self(), files[current_idx]);
        results[current_idx] = stretch_hash(files[current_idx]);
    }
    return NULL;
}

int main(int argc, char** argv) {
    int max_threads = (argc > 1) ? atoi(argv[1]) : 2;
    if (max_threads <= 0) max_threads = 1;

    printf("Pornim procesarea a %d fisiere folosind maxim %d thread-uri...\n\n", num_files, max_threads);

    pthread_t* threads = malloc(max_threads * sizeof(pthread_t));

    for (int i = 0; i < max_threads; i++) {
        pthread_create(&threads[i], NULL, worker_routine, NULL);
    }

    for (int i = 0; i < max_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("\n--- Rezultate finale ---\n");
    for (int i = 0; i < num_files; i++) {
        printf("File %s checksum: %lu\n", files[i], results[i]);
    }

    free(threads);
    pthread_mutex_destroy(&mock_mutex);
    return 0;
}