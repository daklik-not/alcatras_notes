**PThreads** - стандарт Posix для потоков.
![[Pasted image 20251101195925.png]]
**thread_id = pthread_create**  - создание потока, thread_id id новосозданного потока.
**pthread_exit** - завершение потока, очищение его стека.
**pthread_join**(pfwaiting) - поток ждет завершение какого-то другого потока
**pthread_yeild**(pfgive) - добровальная передача своего процессорного времени другому потоку
**pthread_attr_init** - создает структуру атрибутов потока. Например так хранится приоритет потока. Важно отметить, что структура атрибутов хранится только на момент инициализации процессов. Затем ее следует удалить.
Пример программы на C
```
void *print_hello_world(void *tid) {
    /* This function prints the thread's identifier and then exits. */
    printf("Hello World. Greetings from thread %ld\n", (long)tid);
    pthread_exit(NULL);
}
int main(int argc, char *argv[]) {
    /* The main program creates 10 threads and then exits. */
    pthread_t threads[NUMBER_OF_THREADS];
    int status, i;
    for(i = 0; i < NUMBER_OF_THREADS; i++) {
        printf("Main here. Creating thread %d\n", i);
        status = pthread_create(&threads[i], NULL, print_hello_world, (void *)(long)i);
        if (status != 0) {
            printf("Oops. pthread_create returned error code %d\n", status);
            exit(-1);
        }
    }
    // Wait for all threads to complete
    for(i = 0; i < NUMBER_OF_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    printf("All threads completed.\n");
    return 0;
}
```