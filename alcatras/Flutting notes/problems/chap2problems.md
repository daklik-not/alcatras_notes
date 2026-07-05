1. In Fig. 2-2, three process states are shown. In theory, with three states, there could be six transitions, two out of each state. However, only four transitions are shown. Are there any circumstances in which either or both of the missing transitions might occur?
Из готового состояния в заблокированное сам по себе процесс не может перевестись. Он может сделать это только, если процесс, который сейчас в работе, пошлет ему сигнал SIGSTOP.  Из заблокированного в готовый переход невозможен впринципе - все системные вызовы вроде wakeup(pid) сначала переводят в готовое состояние, а не принудительно запускают

2. Suppose that you were to design an advanced computer architecture that did process switching in hardware, instead of having interrupts. What information would the CPU need? Describe how the hardware process switching might work.

Процессору необходимы 3 элемента - program counter - последняя инструкция, program status word -  состояние процессора(например значение последней логической инструкции) и stack pointer - указатель на стек процесса, мы должны иметь доступ к его данным, pid - идентификатор процесса, state - чтобы понимать, какие процессы не нужно запускать и впринципе  состояние того или иного процесса
В моей системе эти 3 элемента будут хранится в SRAM.
Также для того, чтобы MMU мог переводить виртуальные адреса в реальные, ему нужна карта памяти процесса. Вообще про это подробно будет в следующей главе книги, так что я не хотел бы сейчас в это закапываться
Создадим структуру аналогичную process table с ее PCB. Она нужна для реализации random lottey
Process switch
	1) Из-за вызова yeild() процессор понимает, что ему надо делать смену контекста
	2) Загружаем текущие значение программного счетчика, program status word,  pid и указатель на стек процесса В SRAM память и регистры общего назначения и его карту памяти(далее буду называть все это состоянием процесса) - все это полный аппаратный контекст PCB
	3) На процессоре в моей системе будет установлен планировщик lottery. Рандомно будем выбирать из process table pid процесса.(только READY процессы) Сама Process table хранится в SRAM памяти
	4) После того, как процесс выбран загружаем ИЗ SRAM состояние нужного процесса и меняем его состояние на RUNNING

3. On all current computers, at least part of the interrupt handlers are written in assembly language. Why?
	  Вектор прерываний это аппаратный механизм. Мы напрямую взаимодействуем с ним, то есть, с аппаратным обеспечением - важна точность и надежность.Также, например на C мы не можем напрямую менять регистры процессора - а это требуется всегда
4. 4. When an interrupt or a system call transfers control to the operating system, a kernel stack area separate from the stack of the interrupted process is generally used. Why?
	Вообще они вроде бы всегда разделены. Сделано это, как мне кажется, для уменьшения количества уязвимостей в системе. Путем четкого разграничения места, где хранятся важные системные данные о процессе, и пользовательского стека мы уменьшаем вероятность того, что злоумышленник может эксплуатировать стек ядра в своих целях - на нем хранится много системной информации о процессе. Также пользовательский код никак не может навредить системе из-за такого четкого разделение
5. Acomputer system has enough room to hold four programs in its main memory. These programs are idle waiting for I/O half the time. What fraction of the CPU time is wasted?
	1/16;
6. A computer has 2 GB of RAM of which the operating system occupies 256 MB. The processes are all 128 MB (for simplicity) and have the same characteristics. If the goal is 99% CPU utilization, what is the maximum I/O wait that can be tolerated?
	Здесь p - вероятность того, что процесс будет ждать. Просто решить это:
		$$max\_processes = (2 * 1024 - 256) / 128$$
		$$(1 - (p) ^ {max\_processes}) * 100 >= 99$$
		
7. Multiple jobs can run in parallel and finish faster than if they had run sequentially. Suppose that two jobs, each needing 10 minutes of CPU time, start simultaneously. How long will the last one take to complete if they run sequentially? How long if they run in parallel? Assume 50% I/O wait.
	Если они будут работать последовательно, то  40 минут, потому что - первый процесс работает 10 минут, затем 10 минут ждет, так же второй.
	 Если параллельно то нужна формула утилизации
	 $$cpu\_utilization = (1 - p^{n}) = 0.75$$
	 Если полезной работы 20, то вся работа:
	 $$ 20 / cpu\_utilization == 26.67$$
	Это все время затраченное процессором
8. Consider a multiprogrammed system with degree of 5 (i.e., fiv e programs in memory at the same time). Assume that each process spends 40% of its time waiting for I/O. What will be the CPU utilization?
	$$ cpu\_utilization = 1 - {2/5}^{5}$$
9. Explain how a Web browser can utilize the concept of threads to improve performance.
Самый простой пример - потоки используются внутри процесса, чтобы при блокировке на IO весь процесс не блокировался, а только 1 его поток. Тогда 1 поток спит на IO, пока другой поток, например, делает какие-то вычисления

10. Assume that you are trying to download a large 2-GB file from the Internet. The file is available from a set of mirror servers, each of which can deliver a subset of the file’s bytes; assume that a given request specifies the starting and ending bytes of the file. Explain how you might use threads to improve the download time.
Для каждого сервера создать свой поток. Так как данные на разных машинах, нужно использовать метод message passing. Каждый поток получив данные, будет записывать в общий файл, которая для взаимного исключения будет ограничена, например, мьютексами. Это важно, чтобы соблюдалась синхронизация - байты файла делались по порядку(deepseek пишет, что потоки  помощью специльаного метода будут записывать сами в нужное место буфера, так что это необязательно) и потоки не перезаписывали друг-друг
11. In the text it was stated that the model of Fig. 2-10(a) was not suited to a file server using a cache in memory. Why not? Could each process have its own cache?
У каждого процесса своя виртуальная память. Он можем кэшировать только в свою виртуальную память. В файловом сервере каждый процесс обслуживает своего клиента. Если двум клиентам понадобится файл 2 раза, и оба раза файлов не будет в кэше, то файлй просто кэшируется 2 раза, потому что 1 процесс не знает про кэш другого
Теоретически можно дать каждому процессу свой кэш. Но это приведет к подобному копированию, как я писал выше, увеличению промахов.  Так же необходимы ресурсы на реализацию межпроцессного взаимодействия для обеспечения взаимного исключения. Это очень медленно - кэш теряет весь свой смысл
12. In Fig. 2-8, a multithreaded Web server is shown. If the only way to read from a file is the normal blocking read system call, do you think user-level threads or kernel-level threads are being used for the Web server? Why?
		Kernel-level threads или вообще гибридные. Если использовать чистые пользовательские, то при блокировке на IO весь процесс обслуживания будет вставать, так как ядро не знает о пользовательских процессах
13. In the text, we described a multithreaded Web server, showing why it is better than a single-threaded server and a finite-state machine server. Are there any circumstances in which a single-threaded server might be better? Give an example.
		Если говорить о однопоточном сервере, но не конечном автомате, то в таком случае все все блокировки будут производиться этим же потоком. Таким образом мы теряем очень много времени. Тогда чтобы такой сервер был эффективен должно быть мало IO и мало клиентов
		Я придумал следующий пример - использовать сервер, как вычислительную мощность. Например факторизация больших чисел. Клиент арендует сервер на какое-то время, загружает его нагрузкой, после чего приходит новый клиент. В этом случае время потраченное на блокирующий системный вызов не столь существенно
14. In Fig. 2-11 the register set is listed as a per-thread rather than a per-process item. Why? After all, the machine has only one set of registers.
			Потому что внутри одного процесса потоки также меняются Эти регистры показывают именно состояние потока а не процесса. При thread_swtich низкоуровневый код загружает состояние регистров нового потока  в процессор.
15. Why would a thread ever voluntarily give up the CPU by calling thread yield? After all, since there is no periodic clock interrupt, it may never get the CPU back.
		Потоки внутри одного приложения могут отдавать друг-другу процессорное время для того, чтобы само приложение работало корректно.
		Если брать user-level потоки, то у них любое переключение между потоками построено засчет thread_yeild(). Без отдачи процессорного времени, приложения программиста просто не будет работать - это в его интересах. Если брать kernel-level - то добровольная передача при долгих вычислениях или блокирующем системном вызове возможна только, если это архитектурное требование.
16. In this problem, you are to compare reading a file using a single-threaded file server and a multithreaded server. It takes 15 msec to get a request for work, dispatch it, and do the rest of the necessary processing, assuming that the data needed are in the block cache. If a disk operation is needed, as is the case one-third of the time, an additional 75 msec is required, during which time the thread sleeps. How many requests/sec can the server handle if it is single threaded? If it is multithreaded?
	1. Используем мат-ожидание. Вероятность того, что понадобится диск - 1/3. Вероятность что нет - 2/3. Тогда мат-ожидание одного процесса при последовательном - $2/3 * 15 + 1/3 * (15 + 75) = 10 + 30 = 40$ . Разделим $100 / 40 = 25$ - ответ
	2. Пропускная способность определяется диском. Если треть своего времени проводится диском за 75 ms. Допустим запросы приходят раз в k секунд. Тогда k/3 они времени проводят в диске. Чтобы диск мог справится - $1000 / 75 - 13.3$.   Тогда интенсивность запросов должна быть - $13.3 * 3 = 40$
		
17. What is the biggest advantage of implementing threads in user space? What is the big gest disadvantage?
		Самое большое преимущество это их скорость. Потоки в пользовательском пространстве не требуют системного вызова при смене, создании или остановке. Они не падают в ядро. Самый большой недостаток - их невозможно использовать с блокирующим IO. Система не знает о таких потоках, поэтому она заблокирует весь процесс со всеми потоками.
18. In Fig. 2-14 the thread creations and messages printed by the threads are interleaved at random. Is there a way to force the order to be strictly thread 1 created, thread 1 prints message, thread 1 exits, thread 2 created, thread 2 prints message, thread 2 exists, and so on? If so, how? If not, why not?
	Да, после создания каждого потока(pthread_create) вызывать pthread_join(). Так мы будем ждать пока дочерний процесс не завершится, и только потом продолжать работу
19. Consider a program with two threads, each executing the `get_account` function shown below. Identify the **race condition** present in this code
```
int accounts[LIMIT];
int account_count = 0;

void *get_account(void *tid) {
    char *lineptr = NULL;
    size_t len = 0;

    while (account_count < LIMIT) {
        // Read user input from terminal and store it in lineptr
        getline(&lineptr, &len, stdin);

        // Convert user input to integer
        // Assume the user always enters a valid integer
        int entered_account = atoi(lineptr);

        accounts[account_count] = entered_account;
        account_count++;
    }

    // Deallocate memory allocated by getline
    free(lineptr);
    return NULL;
}
```
 Потоки будут перезаписывать буфер account и глобальную переменную account_count. 
 
 20. In the discussion on global variables in threads, we used a procedure create global to allocate storage for a pointer to the variable, rather than the variable itself. Is this essential, or could the procedures work with the values themselves just as well?
Мой ответ - я не уверен, что он полностью неправильный
Здесь речь о глобальных переменных одного потока.  Мы можем использовать значения а не ссылки, но тогда по затратам памяти это просто будет эквивалентно тому, что мы будем в каждый вызов любой функции передавать все параметры. Так что это просто не  эффективно
Ответ нейронки:
Использование указателя в механизме `create_global`/`set_global`/`read_global` является существенным, потому что этот механизм должен поддерживать переменные любого типа и размера. Указатель имеет фиксированный размер, что позволяет системе управлять слотами единообразно. Если бы мы хранили значения напрямую, потребовалось бы знать размер каждого типа на этапе создания переменной, что сделало бы механизм менее гибким и более сложным в реализации.

21. Consider a system in which threads are implemented entirely in user space, with the run-time system getting a clock interrupt once a second. Suppose that a clock interrupt occurs exactly while some thread executing in the run-time system is at the point of blocking or unblocking a thread. What problem might occur? Can you solve it?
	Допустим  runtime система добавила поток на очередь потоков, но еще не поменяла его состояние. Если в этот момент произойдет прерывание, то планировщик увидит некорректное состояние - поток и не рабочий, и не заблокирован. Тогда он примет некорректное решение. Чтобы решить это можно либо блокировать сигналы от ядра на время, пока runtime находится в критическом сегменте. Либо можно сделать операцию, которая будет атомарная, и в которой мы будем одновременно и класть на очередь и менять состояние.
22.  22. Suppose that an operating system does not have anything like the select system call to see in advance if it is safe to read from a file, pipe, or device, but it does allow alarm clocks (timers) to be set that interrupt blocked system calls. Is it possible to implement in user space a threads package that will not block all threads when one thread per forms a system call that may block? Explain your answer.
	В теории да, можем. Тогда если операция системного вызова выполняется больше какого-то количества времени, то мы прерываем системный вызов - разблокируем все потоки в пользовательском пространстве.  Фактически потоки будут блокироваться, но на значительно меньшее количество времени.  В пакете потоков нужно добавить код, который будет обрабатывать эти прерывания, то есть просто блокироваться
	У такого подхода есть проблемы. Мы не определяем раз в сколько времени приходят прерывания. Допустим read() не заблокировался, но просто читает очень много данных в RAM. Тогда он может быть прерван просто потому, что долго работает. 
	Deepseek: Некоторые системные вызовы могут оставлять данные в неопределенном состоянии - небезопасно прерываются.
23. Does Peterson’s solution to the mutual-exclusion problem shown in Fig. 2-24 work when process scheduling is preemptive? How about when it is nonpreemptive
При non-preemptive планировании потоков фактически ничем не отличается от строгого чередования, поскольку потоки выполняются один за другим, но тем не менее оно работает. При preemptive планировании он работает только для 2 потоков. Если потоков больше, то алгоритм Питерсона ломатся
24. Can the priority inversion problem discussed in Sec. 2.3.4 happen with user-level threads? Why or why not?
		Проблема приоритета не зависит от типов потоков. В пользовательском пространстве так же работает планировщик. Если поток с низким приоритетом находится в критическом сегменте, а высокий не в критическом сегменте, низкий никогда не запустится, а высокий никогда не войдет в критический сегмент
25. In Sec. 2.3.4, a situation with a high-priority process, H, and a low-priority process, L, was described, which led to H looping forever. Does the same problem occur if round robin scheduling is used instead of priority scheduling? Discuss
		Нет, потому что каждому потоку выделен определенный квант времени. Тогда даже если round-robin сделан с учетом приоритетов, то вечного цикла не будет
26. In a system with threads, is there one stack per thread or one stack per process when user-level threads are used? What about when kernel-level threads are used? Explain.
		В kernel-level потоках у каждого потока свой стек
		В user-level потоках у каждого процесса 1 стек, реализованный в ядре(не стек ядра).  Однако, у каждого потока свой стек, реализованный в пользовательском пространстве
27. What is a race condition?
	Race condition - состояние гонки. Оно возникает, когда у потоков или процессов есть доступ к 1 памяти. Из-за того, что аппаратные прерывания могут прийти в любой момент, потоки-процессы могут работать не с актуальными значениями. Решение требует специальных механизмов синхронизации и взаимного исключения
28. When a computer is being developed, it is usually first simulated by a program that runs one instruction at a time. Even multiprocessors are simulated strictly sequentially like this. Is it possible for a race condition to occur when there are no simultaneous ev ents? Explain.
		Да может. Она возникает если процессы не синхронизированы между собой и имею доступ к общей памяти. Если более точно, то в данной симуляции порядок выполнения не определен. Если 2 процесса увеличивают значение общей переменной g, то мы не знаем сколько раз каждый поток увеличит переменную. 
29. The producer-consumer problem can be extended to a system with multiple producers and consumers that write (or read) to (from) one shared buffer. Assume that each pro ducer and consumer runs in its own thread. Will the solution presented in Fig. 2-28, using semaphores, work for this system?
```
    #define N 100 typedef int semaphore; semaphore mutex = 1; /* number of slots in the buffer */ 131 /* semaphores are a special kind of int */ semaphore empty = N; semaphore full = 0; void producer(void) { int item; while (TRUE) { item = produce item( ); down(&empty); down(&mutex); inser t item(item); up(&mutex); up(&full); } } void consumer(void) { int item; while (TRUE) { down(&full); down(&mutex); item = remove item( ); up(&mutex); up(&empty); consume item(item); } }
```
Да. Пока семафор mutex  = 1, ни один из потоков не зайдет в критический регион.  Также  если семафоры full и empty то соответствующие им потоки будут блокироваться.

30. Consider the following solution to the mutual-exclusion problem involving two proc esses P0 and P1. Assume that the variable turn is initialized to 0. Process P0’s code is presented below.
```
/* Other code 
*/ while (turn != 0) { } 
/* Do nothing and wait. 
*/ Critical Section
turn = 0; 
/* Other code */
```

For process P1, replace 0 by 1 in above code. Determine if the solution meets all the required conditions for a correct mutual-exclusion solution.
По Таннебауму 4 		
1. Мы не должны полагаться на время выполнения процессором - выполняется в данном коде
2.  Никакой процесс, находящийся не в критическом регионе не может блокировать любой другой процесс - не выполняется, поскольку сразу после того, как поток закончил критическую секцию, может произойти прерывание и тогда turn  = 0 а поток уже другой.
3. Никакой процесс не должен ждать бесконечно своего вхождение в критический регион -не  выполняется, это очень медленно, поскольку если после критической секции одного потока произойдет смена контекста, то другой поток, который хочет попасть в критическую секцию будет ждать, пока планировщик снова не выберет первый поток. Короче говоря нет никаких гарантий что он вообще ее получит.
4.  Никакие 2 процесса не находятся в их критическом регионе - выполнятся. Это строгое чередование

Вообще решение рабочее, но очень медленно
31.  Show how counting semaphores (i.e., semaphores that can hold an arbitrary value) can be implemented using only binary semaphores and ordinary machine instructions.
```c
binary_semaphore m(1);//для защиты переменной counter
binary_semaphore d(0);//для очереди
struct countingsem {
    int counter = 0; // счетчик wake-up() битов
    void up() {
        m.acquire(); // критическая секция
        counter++; // попытались разбудить - запомнили wake-up()
        if (counter <= 0) d.release(); // сразу пытаемся разбудить какой-то поток
        m.release(); // конец критической секции
    }
    void down() {
        m.acquire(); // критическая секция
        counter--; // потоку надо заблокироваться
        if (counter < 0) { // если нет сохранненых wakeup битов
            m.release();// конец критической секции
            d.acquire(); // блокируем
        } else {
             m.release(); // конец критической секции
        }
    }
};
```

31. If a system has only two processes, does it make sense to use a barrier to synchronize them? Why or why not?
	Имеет, просто это будет тривиальная реализация. Можно реализовать через, например семафоры
32. Can two threads in the same process synchronize using a kernel semaphore if the threads are implemented by the kernel? What if they are implemented in user space? Assume that no threads in any other processes have access to the semaphore. Discuss your answers.
	Если kernel-level потоки, то можно. Ядро знает о kernel-level потоках. Если потоки в пользовательском пространстве, то нельзя. Система просто не знает о существовании каких-то потоков в пользовательском пространстве, поэтому заблокирует весь процесс.
33. Suppose that we have a message-passing system using mailboxes. When sending to a full mailbox or trying to receive from an empty one, a process does not block. Instead, it gets an error code back. The process responds to the error code by just trying again, over and over, until it succeeds. Does this scheme lead to race conditions?
	Да. Например как вот здесь
	```c
void writer() {
    if (mailbox.size() != N) {
        //вот здесь может произой
        mailbox.push(el);
    }
}
	```
34. The CDC 6600 computers could handle up to 10 I/O processes simultaneously using an interesting form of round-robin scheduling called processor sharing. A process switch occurred after each instruction, so instruction 1 came from process 1, instruc tion 2 came from process 2, etc. The process switching was done by special hardware, and the overhead was zero. If a process needed T sec to complete in the absence of competition, how much time would it need if processor sharing was used with n proc esses?
		Каждый процесс будет выполняться время приблизительно равное суммарному времени выполнения всех процессов.
		Если процесс в одиночку выполняется за T секунд, то при processor sharing с n процессами он будет выполняться n × T секунд. - то же самое но чуть сложнее
		
35. Consider the following piece of C code: void main( ) { fork( ); fork( ); exit( ); } Howmanychild processes are created upon execution of this program?
	Оказывается после вызова fork() - именно пустого - программа начинает выполнение с следующей строчки. Таким образом 3 дочерних процесса.
	![[Pasted image 20251216210436.png]]
36. Round-robin schedulers normally maintain a list of all runnable processes, with each process occurring exactly once in the list. What would happen (scheduling-wise) if a process occurred twice in the list? Can you think of any reason for allowing this?
	Процесс получит больше квантов времени. Это может быть использовано для реализации приоритетов
		
37. Can a measure of whether a process is likely to be CPU bound or I/O bound be deter mined by analyzing source code? How can this be determined at run time?
		Нет не можем. Мы не знаем, о том, какого размера данные DMA перекачивает с IO в RAM. Однако мы можем что-то предположить на основе того какой код. Например если в коде много вычислений или наоборот много IO(хотя это ничего не гарантирует, поскольку IO может быть быстрым) Во время запуска каждый раз при перепланировании мы можем смотреть, сколько времени процесс провел в заблокированном состоянии(не в готовом), и на этой основе что--то предполагать
38. In the section ‘‘When to Schedule,’’ it was mentioned that sometimes scheduling could be improved if an important process could play a role in selecting the next process to run when it blocks. Give a situation where this could be used and explain how
		Скорее всего это улучшает ситуацию поскольку разработчик приложения лучше знает, как планировать свои процессы чем ядро ОС. Например рассмотрим классический пример веб-сервера. Если процесс будет планировать так, чтобы у диспетчера был приоритет выше чем у рабочего, это значительно повысит эффективность
39. Explain how time quantum value and context switching time affect each other, in a round-robin scheduling algorithm.
	Чем меньше квантум времени, тем больше происходит смен контекста. Смена контекста - тяжелая операция. Таким образом из-за маленького квантума времени будет понижаться производительность. Насколько я знаю, чаще всего процессы будут блокироваться значительно раньше чем выделенная часть времени. Он нужен, чтобы никакой процесс не ломал системы своим долгим запуском
40. Measurements of a certain system have shown that the average process runs for a time T before blocking on I/O. A process switch requires a time S, which is effectively  wasted (overhead). For round-robin scheduling with quantum Q, giv e a formula for the CPU efficiency for each of the following
		(a) Q = inf - T/(T + S), но если зависает, то 0%
		(b) Q > T  - T/(T + S), , но если 1 процесс зависает, то не но % поскольку система продолжит работать
		(c) S < Q < T,  T / ( (T / Q) * (S +Q) + T%Q + S) или (T / ( T + ceil(T / Q) * S)
		d) Q = S
			Если T < Q:
				= T/ (T + S)
			Если T > Q:
				= T / (T  + ceil(T / Q) * S)
		(e) Q nearly 0 - 0%
41. Five jobs are waiting to be run. Their expected run times are 9, 6,0 3, 5, and X. In what order should they be run to minimize average response time? (Your answer will depend on X.)
		Запускать по неубыванию времени выполнения.  Позиция икса будет определяться как upperbound
 42.  Five batch jobs, A through E, arrive at almost the same time. They have estimated run ning times of 10, 6, 2, 4, and 8 minutes. Their (externally determined) priorities are 3, 5, 2, 1, and 4, respectively, with 5 being the highest priority. For each of the following scheduling algorithms, determine the mean process turnaround time. Ignore process switching overhead
      (a) Round robin. (b) Priority scheduling. (c) First-come, first-served (run in order 10, 6, 2, 4, 8). (d) Shortest job first. 
      For (a), assume that the system is multiprogrammed, and that each job gets its fair share of the CPU. For (b) through (d), assume that only one job at a time runs, until it finishes. All jobs are completely CPU bound.
    
      a) (10 +18 + 24 + 28 + 2) / 5 = 22
      b)(6 + 14 + 24 + 26 + 30) /  5 = 20
      c)(10 + 16 + 18 + 22 + 30) / 5 =  19.2
      d) (2 + 6 + 12 + 20 + 30) / 5 = 14
43. A process running on CTSS needs 30 quanta to complete. How many times must it be swapped in, including the very first time (before it has run at all)?
		В CTSS процесс изначально запускается с 1 квантом времени. И после каждого понижения ему дают в 2 раза больше квантов времени. Тогда  - 1 + 2 + 4 + 8 + 16. Тогда 5 раз
44. Can you think of a way to save the CTSS priority system from being fooled by random carriage returns?
		Суть проблема в том, что в системе подряд активировали множество коротких ничего не значащих процессов. Каждому из них выдавался высокий приоритет. Очевидно,это сильно замедляло важные процессы.
		Можно было бы давать определенное количество квантов времени для каждого пользователя. Мы знаем кому принадлежит процесс - можно ограничить количество выделяемых квантов для пользователя.  Также можно использовать следующий подход - оценивать приоритет процесса и по тому, сколько процессорного времени он потребил. Если много - понижаем приоритет, если мало, то повышаем. Однако это работает только если у одного пользователя один процесс. В противном случае, нужно ограничение на количество процессов для пользователя
45. Consider a real-time system with two voice calls of periodicity 5 msec each with CPU time per call of 1 msec, and one video stream of periodicity 33 msec with CPU time per call of 11 msec. Is this system schedulable? Show how you derived your answer.
			$$ 2 / 5 + 11 / 33 = 0.73 <= 1   -- schedulable$$
46. For the above problem, can another video stream be added and have the system still be schedulable?
		Нет, будет > 1;
47. The aging algorithm with a = 1/2 is being used to predict run times. The previous four runs, from oldest to most recent, are 40, 20, 40, and 15 msec. What is the prediction of the next time?
		$EstT_{new} = aT_{old} +(1 - a) T_{measured}$
		По вот этой формуле посчитать, для второго процесса $T_{old} =40, T_{meas} = 40$
		Ответ 26.25(У  меня чуть все сьехало, но в целом логика правильная так что норм)
 48. A soft real-time system has four periodic events with periods of 50, 100, 200, and 250 msec each. Suppose that the four events require 35, 20, 10, and x msec of CPU time, respectively. What is the largest value of x for which the system is schedulable?
		 12.5, если используется EDF
49. Explain why two-level scheduling is commonly used. What advantages does it have over single-level scheduling?
    Смысл two-level scheduling в том, что нижний уровень загружает процессор, выбирает, какой процесс будет запущен. Это может быть обычный round-robin. Тем не менее в оперативной памяти может находиться только опредленное количество процессов. Высокоуровненый планировщик меняет местами долго запущенные процессы в RAM и процессы с диска, которые долго не запускались.
    Плюс такого подхода, во-первых в разделении обязанностей - повышении безопасности и отказоустойчивости. Операции подкачки и запуска на процессоре разительно отличаются по количеству затраченного времени. Поэтому и нужно разделение - для повышени яяэффек
50.   51. A real-time system needs to handle two voice calls that each run every 5 msec and con sume 1 msec of CPU time per burst, plus one video at 25 frames/sec, with each frame 178 PROCESSES AND THREADS CHAP. 2 requiring 20 msec of CPU time. Is this system schedulable? Please explain why or why not it is schedulable and how you came to that conclusion.
		Сколько раз буде запущен первый voice call - 1000 / 5* 2 = 400ms
		Сколько времени надо чтобы обработать 25 кадров в секунду  -  20 * 25 = 500
		500 + 400 = 900
		900 < 1000 -> система schedulable
51. Consider a system in which it is desired to separate policy and mechanism for the scheduling of kernel threads. Propose a means of achieving this goal.
		Политикой, например расставлением приоритетов потоков, будет заниматься один планировщик. Другой будет просто выполнять context switch или вытеснять процессы.
52. The readers and writers problem can be formulated in several ways with regard to which category of processes can be started when. Carefully describe three different variations of the problem, each one favoring (or not favoring) some category of proc esses (e.g., readers or writers). For each variation, specify what happens when a reader or a writer becomes ready to access the database, and what happens when a process is finished.
	1. всегда отдается приоритет читателям
		Если в критической секции находится писатель, то процесс  не может быть запущен. Если читатель, или там никого нет, то процесс может запуститься в любой момент. После завершения процесса запустится другой читатель, если такой есть, и писатель, если читателей больше нет. Важно, что под блоком подразумеваются все готовые процессы читателей, в данном случае.
	2. всегда отдается приоритет писателей
		Если в критической секции уже находится какое-то количество читателей, то он должен закончить работы и освободить мьютекс. Однако после него сразу будет запущен процесс писателя. После завершения процесса писателя - если есть доступные писатели будет запущен писатель, если нет, то блок читателей
	3. нет приоритета - first come-first served
			Будет выбираться тот процесс,  который первый будет в очереди FIFO. То же самое после завершения процесса.
53. Write a shell script that produces a file of sequential numbers by reading the last num ber in the file, adding 1 to it, and then appending it to the file. Run one instance of the script in the background and one in the foreground, each accessing the same file. How long does it take before a race condition manifests itself? What is the critical region? Modify the script to prevent the race. (Hint: use ln file file.lock to lock the data file.)  
Сам скрипт. В моем случае, сначала race condition произошел на числе 2. Но во всех запусках по разному  
```c  
#!/bin/bash  
for i in {1..20}; do  
content=$(tail -n 1 file.txt)  
numtoadd=$((content+1))  
echo $numtoadd >> file.txt  
done  
  
#./script.sh & ./script.sh $ - в консоли запускал этой командой  
```  
Здесь критический регион - сам файл.  
Чтобы решить это использует flock  
```c  
#!/bin/bash  
LOCKID=200  
file=mutex.lock  
eval "exec $LOCKID>$file"  
for i in {1..20}; do  
flock -x 200  
content=$(tail -n 1 file.txt)  
numtoadd=$((content+1))  
echo $numtoadd >> file.txt  
flock -u 200  
done  
```  
55.  Assume that you have an operating system that provides semaphores. Implement a message system. Write the procedures for sending and receiving messages.  
```c  

struct Message {
    static const int defaultLength = 32;
    char buff[defaultLength + 1];
};

static char* mailbox(char* name, const int mailsize) {
    bool isNewMailBox = false;
    int shm = shm_open(name, O_RDWR, S_IRWXO|S_IRWXG|S_IRWXU);
    if (shm == -1) { // почтовый ящик еще не создан
        isNewMailBox = true;
        shm = create_mailbox(name, mailsize);
        if (shm == - 1) {
            std::cerr << "Error in creating mailbox";
            return nullptr;
        }
    }
    //теперь добавим память почтового ящика к адресному пространству процесса
    char *addr = (char*) mmap(nullptr, mailsize + 1,PROT_WRITE|PROT_READ, MAP_SHARED, shm, 0);
    //nullptr - ОС сама решит, какой адрес будет. PROT_WRITE|PROT_READ - разрешить чтение и запись
    //MAP_SHARED - изменения видны другим процессам. 0 - смещения.
    //mmap - выделение динамической памяти на стеке программы
    if (addr == (char*)-1) {
        std::cerr << "cant get mailbox";
        return nullptr;
    }
    //если это новосозданный почтовый чщик, то в первые 2 слота кладем служебную инфу
    if (isNewMailBox) {
        ((int*)addr)[0] = mailsize - sizeof(int)*2; //доступный размер, весь - служебный
        ((int*)addr)[1] = 0; // занятых байтов
    }
    return addr;
}

static int create_mailbox(char* name, const int mailsize) {
    int shm = shm_open(name, O_CREAT|O_RDWR,S_IRWXO|S_IRWXG|S_IRWXU);
    //O_CREAT - создать если нет, O_RDWR - открыть на чтение и запись
    //S_IRWXU - права: владелец,S_IRWXG — права: группа (read/write/execute).
    //S_IRWXO — права: другие (read/write/execute).
    if (shm == -1) {
        std::cerr << "Error int creatin mailbox";
    }
    //задаем размер сегмента разделяемой памяти
    int isOk = ftruncate(shm, mailsize);
    if (isOk == -1) {
        std::cerr << "Error in allocating mameory";
    }
    return shm;
}

static sem_t* getSemaphore(char* name) {
    std::string sSem = "/"; // POSIX требует, чтобы имя семафора начиналось с /
    sSem += name;
    sem_t* sem = sem_open(sSem.c_str(), O_CREAT, 0666, 1);
    //0666 - типо числовое значение прав, как для chmod, 1 - исходное значение
    if (sem == (sem_t *)-1) {
        std::cerr << "error in getting sem";
        return nullptr;
    }
    return sem;
}
static int writeMessage(char* name, const int mailsize, char* message, int messageSize) {
    Message msg;
    char* mailboxBuf = mailbox(name, mailsize);
    if (mailboxBuf == MAP_FAILED) return -1;
    int* header = (int*)mailboxBuf;
    int allAvaliableBytes = header[0];
    int takenBytes = header[1];
    int realAvaliableBytes = allAvaliableBytes - takenBytes;
     //не получилось создать или получить доступ к почтовому ящику
    if ((messageSize > msg.defaultLength) || (messageSize > realAvaliableBytes)) return -1; //сообщение слишком длинное.
    for (int i = 0; i < msg.defaultLength; ++i) {
        msg.buff[i] = message[i];
    }
    for (int i = 2 * sizeof(int); i < allAvaliableBytes + sizeof(int) * 2; i+=msg.defaultLength) {
        if (mailboxBuf[i] == 0x00) {
            int it = 0;
            while (it < msg.defaultLength) {
                if (it >= messageSize) mailboxBuf[i + it] = 0x00;
                else mailboxBuf[i + it] = msg.buff[it];
                it += 1;
            }
            header[1] += msg.defaultLength;
            return 0;
        }

    }
    return -1;
}

static int readMessage(char* name, const int mailsize, char* copyto) {
    Message msg;
    char* mailboxBuf = mailbox(name, mailsize);
    if (mailboxBuf == MAP_FAILED) return -1;
    int* header = (int*)mailboxBuf;
    int allAvaliableBytes = header[0];
    int takenBytes = header[1];
    for (int i = sizeof(int) * 2; i < allAvaliableBytes + sizeof(int) * 2; i+= msg.defaultLength) {
        if (mailboxBuf[i] != 0x00) {
            int it = 0;
            while (it < msg.defaultLength) {
                copyto[it] = mailboxBuf[it + i];
                mailboxBuf[it + i] = 0x00;
                it += 1;
            }
            header[1] -= msg.defaultLength;
            return 0;
        }
    }
    return -1;
}
#endif // MAILBOXAPI_H_INCLUDED
static const int defSizeForCreating = 130;
int receive_msg(char* name, char* copyto) {
    sem_t* sem = getSemaphore(name);
    if (sem == nullptr) {
        std::cerr << "error in getting sem";
        return -1;
    }
    sem_wait(sem);
    int result = readMessage(name, defSizeForCreating, copyto);
    sem_post(sem);
    sem_close(sem);
    return result;
}
int send_msg(char* name, char* msg, int messageSize) {
    sem_t* sem = getSemaphore(name);
    if (sem == nullptr) {
        std::cerr << "error in getting sem";
        return -1;
    }
    sem_wait(sem);
    int result = writeMessage(name, defSizeForCreating, msg, messageSize);
    sem_post(sem);
    sem_close(sem);
    return result;
}
#endif // MAILBOXREADYCALLS_H_INCLUDED
```

	
55. Rewrite the program of Fig. 2-23 to handle more than two processes.
```c
while (true)
        while (turn != mythreadid) {}
        critical_region();
        turn = (turn + 1) % N;
        noncritical_region();
    }
```

56. Write a producer-consumer problem that uses threads and shares a common buffer. However, do not use semaphores or any other synchronization primitives to guard the shared data structures. Just let each thread access them when it wants to. Use sleep and wakeup to handle the full and empty conditions. See how long it takes for a fatal race condition to occur. For example, you might have the producer print a number once in a while. Do not print more than one number every minute because the I/O could affect the race conditions.
    ```c
    #include <iostream>
#include <vector>
#include <string>
#include <pthread.h>
#include <signal.h>
using namespace std;

const int N = 5;
char buffer[N];
int consumerUse = 0;
int producerUse = 0;


struct threadArgs {
    pthread_t id;
    char** stackPointer;
};

int freeSlots = N;
void* produce(void* producerArgs) {

    threadArgs *args = (threadArgs*)producerArgs;
    pthread_t consumerID = args->id;
    char** stackPointer = args->stackPointer;

    //создание обработчика сигнала для wakeup();
    sigset_t mask; //создали маску сигналов
    //это типо такая штука, которая хранит все сигналы
    sigemptyset(&mask);// очищаем изначальную маску
    sigaddset(&mask, SIGUSR1); // добавляем в маску сигнал
    pthread_sigmask(SIG_BLOCK, &mask, NULL);//блокируем сигналы, чтобы сигнал не пропадал
     //задали маску
    int sig;
    while (1) {
        usleep(5000000);
        producerUse += 1;
        std::cout << "producerUSE " << producerUse << " freeSlots " << freeSlots << " stack index " << *stackPointer - buffer << std::endl;
        if (freeSlots == 0) {
            pthread_sigmask(SIG_UNBLOCK, &mask, NULL);
            sigwait(&mask,&sig);
            pthread_sigmask(SIG_BLOCK, &mask, NULL);
        }
        if (freeSlots == N - 1) pthread_kill(consumerID, SIGUSR1);
        char** buffPointer = (char**)stackPointer;
        **buffPointer = 'k';
        *buffPointer += 1;
        freeSlots -= 1;
    }

    return nullptr;
}
void* consume(void* consumerArgs) {
    threadArgs *args = (threadArgs*) consumerArgs;
    pthread_t producerID = args->id;
    char** stackPointer = args->stackPointer;
    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGUSR1);
    pthread_sigmask(SIG_BLOCK, &mask, NULL);

    int sig;
    while(1) {
        usleep(5000000);
        consumerUse+=1;
        std::cout << "consumerUse" << consumerUse<< " freeSlots " << freeSlots << " stack index " << *stackPointer - buffer << std::endl;
        if (freeSlots == N) {
            pthread_sigmask(SIG_UNBLOCK, &mask, NULL);
            sigwait(&mask, &sig);
            pthread_sigmask(SIG_BLOCK, &mask, NULL);
        }
        if (freeSlots == 1) pthread_kill(producerID, SIGUSR1);
        char** buffPointer = (char**)stackPointer;
        *buffPointer -= 1;
        freeSlots += 1;
    }

    return nullptr;
}
int main()
{
    char* stackPointer = buffer;
    pthread_t consumerID, producerID;
    threadArgs consumerArgs = {producerID, &stackPointer}, producerArgs = {consumerID, &stackPointer};
    int producerResult = pthread_create(&producerID, nullptr, produce, &producerArgs);
    int consumerResult = pthread_create(&consumerID, nullptr, consume, &consumerArgs);
    usleep(1000000000);
}

    ```
Вот мой код.  У меня они сначала чередовались, потом на cout producer прервалось и сразу segfault. Оценка по дипсику 3/10. Главная ошибка, в реализации буфера. Во-первых должны быть 2 разных указателя для чтения и для записи. Во-вторых, буфер должен быть циклическим. Остальное не очень важно на самом деле. Я не буду переписывать весь код, просто в следующий раз напишу нормально
58. 58. A process can be put into a round-robin queue more than once to give it a higher prior ity. Running multiple instances of a program each working on a different part of a data pool can have the same effect. First write a program that tests a list of numbers for pri mality. Then devise a method to allow multiple instances of the program to run at once in such a way that no two instances of the program will work on the same number. Can you in fact get through the list faster by running multiple copies of the program? Note that your results will depend upon what else your computer is doing; on a personal computer running only instances of this program you would not expect an improvement, but on a system with other processes, you should be able to grab a big ger share of the CPU this way.
```c
#include <iostream>
#include <vector>
#include <unistd.h>
#include <fcntl.h>
#include <chrono>
#include <sys/mman.h>
#include <semaphore.h>
#include <fstream>l
bool isSimple(long long num)
{
    for (long long  i = 2; i * i <= num; ++i)
    {
        if (num % i == 0)
        {
            return false;
        }
    }
   return true;
}
int main()
{  
    auto start = std::chrono::high_resolution_clock::now();
    sem_unlink("/averylongnameforsemaphore");  // Удаляем старый семафор
    shm_unlink("/simple");  
    std::ifstream file("file.txt");
    std::vector<long long>simple;
    long long num;
    while (file >> num) simple.push_back(num);
    char *name = "/simple";
    // выделили разделяемую память
    int shm = shm_open(name, O_CREAT | O_RDWR, S_IRWXO | S_IRWXG | S_IRWXU);

    if (shm == -1)
    {
        std::cerr << "error in creating shared memory";
    }
    int isOk = ftruncate(shm, sizeof(long long));
    if (isOk == -1)
    {
        std::cerr << "error in allocating memory";
    }
    long long *addr = (long long *)mmap(nullptr, sizeof(long long), PROT_WRITE | PROT_READ, MAP_SHARED, shm, 0);
    *addr = 0;
    if (addr == MAP_FAILED)
    {
        std::cerr << "mmap failed" << std::endl;
        return 1;
    }
 // std::cout << *addr << std::endl;
    // перь обьявим семафор на разделяемую память
    char *semaphoreName = "/averylongnameforsemaphore";
     // И старую разделяемую память тоже
    sem_t *sem = sem_open(semaphoreName, O_CREAT, 0666, 1);
    for (int i = 0; i < 10; ++i)
    {
        pid_t result = fork();
        if (result < 0)
        {
            std::cerr << "error in creating process";
        }
        else if (result == 0)
        { // result = 0 -> код дочернего процесс
            // поскольку read-on-write, разделяемая память уже присоедина -> просто читаем ;
            while (1)
            {
                long long lastDone;
                //std::cout << "some code" << std::endl;
                sem_wait(sem);
                //std::cout << "some code" << std::endl;
                lastDone= *addr;
                if (lastDone >= simple.size())
                {
                    auto end = std::chrono::high_resolution_clock::now(); // Конец отсчета
                    std::chrono::duration<double> duration = end - start;
                    std::cout << duration.count() << std::endl;
                    sem_post(sem);
                    exit(0);
                }
                (*addr)++;
                sem_post(sem);
                bool is = isSimple(simple[lastDone]);
            }
            sem_close(sem);
            exit(0);
        }
        else
        {
            sleep(5000);
        }
```
Код примерно вот такой. Основная идея в том, что мы как бы забиваем планировщик round-robin своими процессами и получаем более быстрое время. Проблема в том, что я пишу Linux code,. а на Linux CFS, а не round robin. Также проблема  в том, что это бы лучше работало на больших данных, а не тех, которые выполняются за пару секунд. Оценка по дипсику 5/10, но в целом у меня всенорм, прога работает, и заебись. Но у меня получилось что однопроцессорный код работает быстрее.
59. Implement a program to count the frequency of words in a text file. The text file is partitioned into N segments. Each segment is processed by a separate thread that out puts the intermediate frequency count for its segment. The main process waits until all the threads complete; then it computes the consolidated word-frequency data based on the individual threads’ output.
```c
#include <iostream>
#include <fstream>
#include <filesystem>
#include <thread>
#include <vector>
#include <unordered_map>

const int N = 5;
int fileSize = std::filesystem::file_size("file.txt");
int eachPart = fileSize / N;
int lastPart =  fileSize % N;

void threadFoo(int it, std::unordered_map<std::string,int>*h) {
    std::ifstream file("file.txt");
    int curPos = it * eachPart, prevPosition = it * eachPart;
    char curSymb;

    file.seekg(prevPosition); //функция перескакивания на определенную позицию
    file.get(curSymb);  // читаем символ
    if (curSymb != ' ') { // если находимся не между словами
        std::string rubbishWord; // считаем 1 слово, просто чтобы оставить его предыдущему
        file >> rubbishWord;

    }
    while ((curPos < prevPosition + eachPart) || (it == N - 1 && curPos < prevPosition + eachPart + lastPart)) { //+проверка на остаток
        std::string currentWord;
        curPos = file.tellg(); //tellg - получение позиции в файле в байтах
        if (curPos == -1) return; // конец файла
        file >> currentWord;
        (*h)[currentWord] += 1; //в хэш-таблице меню прибавляют значение слова
    }
}
int main() {
    std::vector<std::thread> threads; //вектор потоков
    std::unordered_map<std::string, int>hashTableArray[N];
    for (int i = 0 ; i < N; ++i) {
        threads.emplace_back(threadFoo, i, &hashTableArray[i]);
    }
    for (size_t i = 0 ; i < threads.size(); ++i) {
        threads[i].join(); // эта штука нужна, чтобы потоки корректно завершались. Иначе у них как вызовется деструктор, который аварийно завершит команду
    }
    std::unordered_map<std::string, int>mainTable;
    for (int i = 0; i <N; ++i) {
        for (auto [key, value] : hashTableArray[i])  mainTable[key] += value;
    }
    // таким образом получится финальная таблица с подсчитанным количеством слов
    for (auto [key, value] : mainTable) std::cout << "key " << key << " " << value << std::endl;
}
```


