#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>

#define ITERS 2000000

const char* files[4] = {"a.html", "b.html", "c.html", "d.html"};
unsigned long results[4];

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

void* thread_routine(void* arg) {
    int idx = *(int*)arg;
    results[idx] = stretch_hash(files[idx]);
    free(arg);
    return NULL;
}

int main(int argc, char** argv) {
    int num_threads = 1;
    if (argc > 1 && strcmp(argv[1], "4") == 0) {
        num_threads = 4;
    }

    if (num_threads == 4) {
        pthread_t threads[4];
        for (int i = 0; i < 4; i++) {
            int* arg = malloc(sizeof(int));
            *arg = i;
            pthread_create(&threads[i], NULL, thread_routine, arg);
        }
        for (int i = 0; i < 4; i++) {
            pthread_join(threads[i], NULL);
        }
    } else {
        for (int i = 0; i < 4; i++) {
            results[i] = stretch_hash(files[i]);
        }
    }

    for (int i = 0; i < 4; i++) {
        printf("File %s checksum simulation: %lu\n", files[i], results[i]);
    }

    return 0;
}