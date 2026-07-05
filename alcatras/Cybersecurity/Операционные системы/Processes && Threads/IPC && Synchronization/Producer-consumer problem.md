**The Producer-Consumer Problem**
Рассмотрим данный пример. Здесь проблема происходит из-за того, что if - неатомарная операция. Допустим $if (count == 1) -> true$. Далее происходит прерывание, после которого теперь работает producer. Он будет еще не спящего потребителя, после чего дополняет до конца буфер и засыпает. Потом работает потребитель -> он тоже блокируется -> оба процесса спят вечно.
```c
#define N 100                /* number of slots in the buffer */
int count = 0;               /* number of items in the buffer */

void producer(void)
{
    int item;
    
    while (TRUE) {           /* repeat forever */
        item = produce_item();  /* generate next item */
        if (count == N) sleep();  /* if buffer is full, go to sleep */
        insert_item(item);    /* put item in buffer */
        count = count + 1;    /* increment count of items in buffer */
        if (count == 1) wakeup(consumer);  /* was buffer empty? */
    }
}

void consumer(void)
{
    int item;
    
    while (TRUE) {           /* repeat forever */
        if (count == 0) sleep();  /* if buffer is empty, go to sleep */
        item = remove_item();   /* take item from buffer */
        count = count - 1;    /* decrement count of items in buffer */
        if (count == N - 1) wakeup(producer);  /* was buffer full? */
        consume_item(item);   /* print item */
    
```
Можно попробовать решить данную проблему через wake-up биты(бит, который нужен, для запоминания wake-up) В таком случае мы достигаем оптимальной реализации для 1-1 consumer-producer проблемы. Однако на более большие случаи она не масштабируется, хотя бы потому, что будет происходить гонка между двумя производителями или двумя потребителями. Это невозможно реализовать wake-up битами.

Теперь рассмотрим решение через семафоры
**Producer consumer problem with semaphores**
Семафоры решают producer consumer проблему. Ниже код с реализацией
```c
semaphore mutex = 1;
semaphore empty = N;
semaphore full = 0;
void producer(void)
{
    int item;
    while (TRUE) {
        item = produce_item();
        down(&empty);
        down(&mutex);
        insert_item(item);
        up(&mutex);
        up(&full);
    }
}
void consumer(void)
{
    int item;

    while (TRUE) {
        down(&full);
        item = remove_item();
        up(&empty);
        consume_item(item);
    }
}
```
Зачем нужен каждый из семафоров?
1. $mutex$ показывает, что в данный момент уже кто-то редактирует буфер. Очевидно мы не хотим, чтобы буфер редактировали и producer и consumer одновременно, не говоря уже о случае с m-k producer-consumer. Если $mutex == 1$ то буфер свободен. Если нет, то нельзя зайти в критическую секцию
2. $empty$  - количество пустых слотов в буфере. Если $empty == 0$ то очевидно producer не может зайти в критическую секцию. Также благодаря тому, что это семафор прерывание не может произойти между if и его выполнением, типо:
```
if (empty == 0) {
	// после условия может пройти прерывания и empty уже будет равен 1.
	// однако благодаря атомарности эти операции неразделимы.
	cout << no_places
}
```
3. $full$ - то же самое
Цели 1 и (2, 3) сильно отличаются.  В то время как первый реализует **mutual exclusion**,  второй и третий реализуют **synchronization**. Синхронизация занимается тем, чтобы гарантировать, что определенная последовательность выполнения процессов не должна произойти. Например здесь, она гарантирует, что producer не положит в уже полностью заполенный буфер.

Теперь рассмотри современное решение через условные переменные и мьютексы

```c
pthread_mutex_t the_mutex;
pthread_cond_t condc, condp;
int buffer = 0;
void* producer(void* ptr) {
    for (int i = 1; i <= MAX; i++) {
        pthread_mutex_lock(&the_mutex);
        while (buffer != 0) // защита от false wakeupов.
            pthread_cond_wait(&condp, &the_mutex);
        buffer = i;
        pthread_cond_signal(&condc);
        pthread_mutex_unlock(&the_mutex);
    }
    return 0;
}
void* consumer(void* ptr) {
    for (int i = 1; i <= MAX; i++) {
        pthread_mutex_lock(&the_mutex);
        while (buffer == 0)
            pthread_cond_wait(&condc, &the_mutex);
        buffer = 0;
        pthread_cond_signal(&condp);
        pthread_mutex_unlock(&the_mutex);
    }
    return 0;
}
int main(int argc, char** argv) {
	// инициализация
    pthread_t pro, con;
    pthread_mutex_init(&the_mutex, 0);
    pthread_cond_init(&condc, 0);
    pthread_cond_init(&condp, 0);
    pthread_create(&con, 0, consumer, 0);
    pthread_create(&pro, 0, producer, 0);
    pthread_join(pro, 0);
    pthread_join(con, 0);
    pthread_cond_destroy(&condc);
    pthread_cond_destroy(&condp);
    pthread_mutex_destroy(&the_mutex);
}
```

Решение Producer-Consumer с помощью мониторов на Java
```c
public class ProducerConsumer {
    static final int N = 100;
    // PROCESSES AND THREADS
    static Producer p = new Producer();   // instantiate a new producer thread
    static Consumer c = new Consumer();   // instantiate a new consumer thread
    static OurMonitor mon = new OurMonitor(); // instantiate a new monitor

    public static void main(String args[]) {
        p.start(); // start the producer thread
        c.start(); // start the consumer thread
    }
    static class Producer extends Thread {
        public void run() { // run method contains the thread code
            int item;
            while (true) { // producer loop
                item = produceItem();
                mon.insert(item);
            }
        }
        private int produceItem() {
            // actually produce
            return 0; // placeholder
        }
    }
    static class Consumer extends Thread {
        public void run() { // run method contains the thread code
            int item;
            while (true) { // consumer loop
                item = mon.remove();
                consumeItem(item);
            }
        }

        private void consumeItem(int item) {
            // actually consume
        }
    }
    static class OurMonitor { // this is a monitor
        private int buffer[] = new int[N];
        private int count = 0, lo = 0, hi = 0; // counters and indices
        public synchronized void insert(int val) {
            if (count == N) goToSleep(); // if the buffer is full, go to sleep
            buffer[hi] = val;            // insert an item into the buffer
            hi = (hi + 1) % N;           // slot to place next item in
            count = count + 1;            // one more item in the buffer now
            if (count == 1) notify();     // if consumer was sleeping, wake it up
        }
        public synchronized int remove() {
            int val;
            if (count == 0) goToSleep(); // if the buffer is empty, go to slee
            val = buffer[lo];            // fetch an item from the buffer
            lo = (lo + 1) % N;           // slot to fetch next item from
            count = count - 1;            // one fewer item in the buffer
            if (count == N - 1) notify(); // if producer was sleeping, wake i
            return val;
        }
        private void goToSleep() {
            try {
                wait();
            } catch (InterruptedException exc) {
            }
        }
    }
}

```

**Producer-consumer problem with Message-Passing**
Общее количество сообщений остается константным. Сначала consumer посылает 10 пустых сообщений producerу.  Сообщения уже отправленные, но еще не полученные буферизируется операционной системой(а именно просто сохраняется в буфер ядра ОС) Если один из них работает быстрее чем другой, то тот, кто работает быстрее будет временно блокироваться. 
Как сообщения адресуются? Можно создать для каждого процесса уникальный адрес, и просто адресовать на него.  Однако такой подход требует четкого последовательного выполнения, как было с strict alternation. Такой подход называется **rendezvous**.
Также можно создать новую структуру данных под названием **mailbox**. Он и у consumer и у producer свой. Это место для буферизации определенного числа сообщений, определенного при создании mailboxa. Параметры в send - адрес mailbox. Если он заполнен, то процесс блокируется. Если нет, то он просыпается.
Ниже код
```c
#define N 100
void producer(void) {
    int item;
    message m;

    while (TRUE) {
        item = produce_item();
        receive(consumer, &m);           // wait for an empty slot
        build_message(&m, item);         // prepare message with item
        send(consumer, &m);              // send message to consumer
    }
}
void consumer(void) {
    int item, i;
    message m;
    // send N empty slots to producer initially
    for (i = 0; i < N; i++) 
        send(producer, &m);
    while (TRUE) {
        receive(producer, &m);           // wait for item from producer
        item = extract_item(&m);         // get item from message
        send(producer, &m);              // return empty slot
        consume_item(item);              // process the item
    }
}

```