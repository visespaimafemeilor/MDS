#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define STEPS 100000

int counter = 0;

void* increment_routine(void* arg) {
    for (int i = 0; i < STEPS; i++) {
        counter++;
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;

    pthread_create(&t1, NULL, increment_routine, NULL);
    pthread_create(&t2, NULL, increment_routine, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Final counter value: %d (Expected: %d)\n", counter, STEPS * 2);

    return 0;
}