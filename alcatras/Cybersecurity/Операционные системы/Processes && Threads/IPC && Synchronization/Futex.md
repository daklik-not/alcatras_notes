# Futex (Fast Userspace Mutex)
## Проблема традиционных подходов
В реализации с `thread_yield` используется подход, близкий к busy-waiting, но более эффективный чем простой spinlock. Busy-waiting хорош при коротких ожиданиях, а sleep-wakeup мьютексы лучше под высокой нагрузкой. Однако оба подхода имеют недостатки:
- **Busy-waiting**: тратит процессорное время
- **Sleep-wakeup**: требует дорогих системных вызовов даже когда блокировка свободна
## Решение: Futex
Futex объединяет преимущества обоих подходов - **быстрый путь** без системных вызовов и **эффективное ожидание** при конкуренции.
**Важно**: 
- Futex - особенность **Linux**, но аналоги существуют в других ОС (Windows: `WaitOnAddress`, macOS: `ulock`)
- Обычный пользователь не работает с futex напрямую - он обернут в библиотеки (pthreads)
- Мьютексы в Linux реализуются через futex
## Как работает futex
### 1. Быстрый путь (Fast Path) - без системных вызовов
Для захвата свободной блокировки используется атомарная операция ( #CAS - Compare-And-Swap). Если блокировка свободна - поток захватывает её **без обращения к ядру**.
### 2. Медленный путь (Slow Path) - эффективное ожидание
Если блокировка занята, поток вызывает `futex(FUTEX_WAIT)` и **блокируется до явного пробуждения**. Это отличается от:
- `thread_yield`: постоянные пробуждения и проверки
- `sleep`: пробуждения по таймеру, а не по событию
## Пример реализации

```c
typedef struct {
    atomic_int state;  // 0 = свободен, 1 = занят
} futex_mutex_t;

void futex_mutex_lock(futex_mutex_t* mutex) {
    // Fast path: пытаемся захватить без syscall
    int expected = 0;
    if (atomic_compare_exchange_strong(&mutex->state, &expected, 1)) {
        return; // Успех! Никакого системного вызова
    }
    
    // Slow path: блокировка занята, переходим к ожиданию
    while (true) {
        // Двойная проверка перед ожиданием
        expected = 0;
        if (atomic_compare_exchange_strong(&mutex->state, &expected, 1)) {
            return;
        }
        // Блокируемся до явного пробуждения
        futex(&mutex->state, FUTEX_WAIT, 1, NULL);
    }
}

void futex_mutex_unlock(futex_mutex_t* mutex) {
    atomic_store(&mutex->state, 0);
    // Будим только если есть ожидающие
    futex(&mutex->state, FUTEX_WAKE, 1, NULL);
}