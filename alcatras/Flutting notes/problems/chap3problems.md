1. In Fig. 3-3 the base and limit registers contain the same value, 16,384. Is this just an accident, or are they always the same? If it is not an accident, why are they the same in this example?
		нет не случайно. base register это начало. limit это сколько байтов от начала принадлежат АП этого процесса. Тогда его граница находится в base + limit.На рисунке конец АП находится в 32764. Тогда с выбранным limit это значит, что процесс просто находится в середине АП

2. In this problem, you are to compare the storage needed to keep track of free memory using a bitmap versus using a linked list. The 8-GB memory is allocated in units of n bytes. For the linked list, assume that memory consists of an alternating sequence of segments and holes, each 1 MB. Also assume that each node in the linked list needs a 32-bit memory address, a 16-bit length, and a 16-bit next-node field. How many bytes of storage is required for each method? Which one is better?
		Количество юнитов - 8,589,934,592/ n. Тогда память под биты битовой карты - 1,073,741,824 / n байт. 
		Для hole списка - (32 + 16 + 16)бита = 8байт.  8\*1024 = 8,192  - количество вершин связанного списка. 8.192 / 2 \ * 8= 32,768 байтов.
		Для вывода - 1,073,741,824 / 32768 <  * n -> 
			Если n > 32КБ, то битовая карта эффективнее по памяти
			Если n < 32КБ, то связный список лучше.
		
3. Consider a swapping system in which memory consists of the following hole sizes in memory order: 10 MB, 4 MB, 20 MB, 18 MB, 7 MB, 9 MB, 12 MB, and 15 MB. Which hole is taken for successive segment requests of (a) 12 MB (b) 10 MB (c) 9 MB for first fit? Now repeat the question for best fit, worst fit, and next fit.
		Next fit начинает искать дырку с того места, где он оставил ее в прошлый раз. Фактически здесь просто будет совпадение с first fit.
		a)12MB:  First-fit - 20MB   best fit - 12MB,  worst fit - 4MB  , .
		b)10MB: First-fit - 10MB  best fit - 10MB ,  worst fit - 20MB , .
		c) 9MB: First-fit - 10MV  best fit - 9MB ,  worst fit  - 20
		Вообще тут оказывается надо последовательно, но мне впадлу переделывать.
4. The first overlay managers and overlay sections were written by hand by programmers. In principle, could this be done automatically by the compiler for a system with limited memory? If so, how, and what difficulties would arise?
		Нужно как-то разбить программу. Основная идея в том, чтобы разбить код на части, которые более-ли-менее изолированы друг от друга. Грубо говоря мы хотим, чтобы процедура из 1 оверлея не вызывала функцию в другом оверлее
			Есть несколько проблем
				1. Перенос адресов. в тексте программы в адресе 1 может быть инструкция вроде jump 60. При этом в адресах 1-60 лежат машинные слова, которые мы не хотим видеть в нашем overlay. Но это вроде несложно решается компилятором - он плотно упаковывает код в адресное пространство
				2.  Если все таки придется доставать адрес из не своего overlay - overlay manager должен как-то решать проблему этих адресов.
				3.  Поиск этих изолированных частей, достаточно трудоемкий
5. 5. In what situations in modern computing might an overlay-style memory system be effective, and why?
		~~Мне кажется в batch системах. Программы огромные - они не могут находится в памяти полностью, при этом малое количество IO bound процессов - следовательно новых данные не будет -> ничего не надо подгружать. Мы просто раз в какое-то время будем менять overlay. (Deepseek сказал, что так было раньше, но сейчас там классическая виртуальная память)~~
		На batch не работает потому, что компилятор не может сам разбивать программу на overlay а самому программисту это делать запарно.
		В embedded системах с малым количеством RAM, и без поддержки MMU. Тогда можно разбивать программу на overlay, чтобы она влазила в память
6. What is the difference between a physical address and a virtual address?
		Физический адрес - адрес где реально в RAM лежат данные.
		Виртуальный адрес-  программная абстракция, которая показывает где лежат данные в другой программной абстракции - виртуальном адресном пространстве. В современных системах виртуальные адреса переводятся в физический
7. For each of the following decimal virtual addresses, compute the virtual page number and offset for a 4-KB page and for an 8-KB page: 20000, 32768, 60000.
		4KB страница занимает offset длиной 12 бит.  8KB страница - 13бит. 
		20000 - 100 111000100000, 4 и 3616.  10 0111000100000 - 2 и  3616
		Аналогично для остальных страниц

8. Using the page table of Fig. 3-9, give the physical address corresponding to each of the following virtual addresses: (a) 2000 (b) 8200 (c) 16536
		То же самое, что в прошлом задании, с учетом того, что страницы размером 4KB. Всего 64К виртуальных адресов - 2^(6 + 10) = 2 ^(16)
		2000 - 0000 011111010000. VPN - 0, offset - 2000.  Для соответствующей VPN - PFN равен 2. Тогда Реальный адрес - 2000 + 8192 = 10192
		Аналогично для остальных
9.  What kind of hardware support is needed for a paged virtual memory to work?
		MMU - для преобразования виртуальных адресов в физические. Также TLB - для большого ускорения работы paging, засчет свойств рабочего набора процеса.
10. Consider the following C program: int X[N]; int step = M; /* M is some predefined constant */ for (int i = 0; i < N; i += step) X[i] = X[i] + 1; (a) If this program is run on a machine with a 4-KB page size and 64-entry TLB, what values of M and N will cause a TLB miss for every execution of the inner loop? (b) Would your answer in part (a) be different if the loop were repeated many times? Explain.
		**10. Рассмотрим следующую программу на языке C:**
		```
			int X[N];
			int step = M;  /* M — некоторая предопределённая константа 
			for (int i = 0; i < N; i += step)
			    X[i] = X[i] + 1;
		```
	**(a)** Если программа выполняется на машине с размером страницы **4 КБ** и **64‑записной TLB**, то при каких значениях **M** и **N** будет возникать **промах TLB при каждом выполнении тела цикла**?
			
	**(b)** Изменится ли ответ в пункте (a), если цикл повторяется много раз? Поясните.
	Ответ: a)Тип int - 4 байта. N / 4 - размер массива в байтах. Чтобы TLB fault происходил каждый раз, нужно чтобы step * sizeof(int) > 4 \*1024, а N > sizeof(int) \* 4\*1024. b) При втором проходе все страницы будут уже в кэше. В таком случае N*sizeof(int) должно быть больше > 64 \* 4KB..  Короче говоря страниц в массиве должно хватить еще на одно выполнение цикла. Далее эти страницы должны полностью перезаписать TLB -  и так по кругу.
 11. The amount of disk space that must be available for page storage is related to the maxi mum number of processes, n, the number of bytes in the virtual address space, v, and the number of bytes of RAM, r. Giv e an expression for the worst-case disk-space requirements. How realistic is this amount?
			Если виртуальное пространство всех процессов будет полностью забито - n\*v - r. Тем не менее такой сценарий полностью не реалистичен, поскольку ОС перестанет выделять память уже когда RAM + swap area будут переполнены.Современные виртуальные АП огромны -> зачастую память одного ап больше чем вся память на диске
12. If an instruction takes 2 nsec and a page fault takes an additional n nsec, give a formula for the effective instruction time if page faults occur every k instructions.
$$(2k + n) / k$$
13. Suppose that a machine has 48-bit virtual addresses and 32-bit physical addresses. (a) If pages are 4 KB, how many entries are in the page table if it has only a single level? Explain.  (b) Suppose this same system has a TLB (Translation Lookaside Buffer) with 32 entries. Furthermore, suppose that a program contains instructions that fit into one page and it sequentially reads long integer elements from an array that spans thou sands of pages. How effective will the TLB be for this case?
		a)Страниц будет 2^(48 - 12) = 2^(36). Но не все будут мапится на страничные кадры.
		b)Достаточно эффективно. В TLB можно хранить как страницы с данными массива, так и страницу с инструкцией. При этом если первый элемент на странице массива вызывает TLB fault - остальные на этой странице не будут. Как только закончатся 31 страница TLB выделенная под это начнут происходить TLB fault. Но опять же - TLB fault только для первого элеметна массива на страни.
14. You are given the following data about a virtual memory system: (a) The TLB can hold 1024 entries and can be accessed in 1 clock cycle (1 nsec). (b) A page table entry can be found in 100 clock cycles or 100 nsec. (c) The average page replacement time is 6 msec. If page references are handled by the TLB 99% of the time, and only 0.01% lead to a page fault, what is the effective address-translation time?
		0.99 * 1 + 0.0001 * (6 * 10^6) + 0.0019 * 100 ~ 601ns
15. Some operating systems, Linux in particular, hav e a single virtual address space, with some set of addresses designated for the kernel, and another set of addresses desig nated for user-space processes. The 64-bit Linux kernel supports a maximum of 4,194,304 processes in the process table, and the kernel is allocated half the virtual address space. If memory address space is divided evenly across all processes, how much virtual address space would be allocated to each process at a minimum, with the maximum number of processes running?
		2^64 байт - максимально возможный размер виртуального адресного пространства Linux. 2^63 - то сколько выделено под процессы. Тогда миниальное адресное пространство - 2^63 / 2 ^ 22 = 2 ^41 байт
16. The 32-bit Linux kernel supports a maximum of 32768 processes in the process table, and the kernel is allocated 1,073,741,824 (1 GiB) of the virtual address space. If mem ory address space is divided evenly across all processes, how much virtual address space would be allocated to each process at a minimum, with the maximum number of processes running?
		2^32 байт - максимально возможный размер виртуального адресного пространства Linux. 2^32 - 2 ^30 - то сколько выделено под процессы. Тогда минимальное адресное пространство - (2^32 - 2^30) / (2 ^ 15) 
17. Section 3.3.4 states that the Pentium Pro extended each entry in the page table hier archy to 64 bits but still could only address only 4 GB of memory. Explain how this statement can be true when page table entries have 64 bits.
		 В нем использовалась трехуровневая таблица - page pointer table содержала 4 вхождений,  page directory содержала 512 вхождений, каждая page table 512 вхождений. Если их перемножить то как раз получиться 4 ГБ.  Процессор генерировал 32 битные виртуальные адреса. При этом общий размер памяти был больше чем 4ГБ -> отсюда и 64битная PTE.
18. A computer with a 32-bit address uses a two-level page table. Virtual addresses are split into a 9-bit top-level page table field, an 11-bit second-level page table field, and an offset. How large are the pages and how many are there in the address space?
		2^32 байт - все адресное пространство
		2^(9 + 11) - количество страниц 
		2^32 / 2^20 = 2^12 байт - 1 страница, или 4КБ - классический размер.
19. Suppose that a 32-bit virtual address is broken up into four fields, a, b, c, and d. The first three are used for a three-level page table system. The fourth field, d, is the offset. Does the number of pages depend on the sizes of all four fields? If not, which ones matter and which do not?
		Число страниц не зависит от offseta. От оффсета зависит размер страницы
		Число страниц зависит от такого какой впринципе максимальный размер адреса поддерживает MMU, и от a+b+c.
20. A computer has 32-bit virtual addresses and 4-KB pages. The program and data toget her fit in the lowest page (0–4095) The stack fits in the highest page. How many entries are needed in the page table if traditional (one-level) paging is used? How many page table entries are needed for two-level paging, with 10 bits in each part?
		Если одноуровневое, то 2^32 / 2^12 = 2^20 вхождений.
		Если двухуровневое, то в памяти только те страницы, которые уже в памяти. 2^10 вхождений в директории + 2^11 вхождений в таблицах страниц -  вся  таблица страниц в директории, если 1 страница в памяти - 3072
21. Below is an execution trace of a program fragment for a computer with 512-byte pages. The program is located at address 1020, and its stack pointer is at 8192 (the stack grows toward 0). Give the page reference string generated by this program. Each instruction occupies 4 bytes (1 word) including immediate constants. Both instruction and data references count in the reference string.
		1)Load word 6144 into register 0 
		1020 >> 9 -> 1 инструкция
		6144 >> 9 -> 12 - данные
		2)Push register 0 onto the stack
		1024 >> 9 -> 2 инструкция
		(8192 - 4) >> 9  -> 15. Вычли 4 потому, что хоть стек и растет вниз, но слова располагаются снизу вверх.
		3)Call a procedure at 5120, stacking the return address
		1028 >> 9 -> 2 - инструкция
		8184 >> 9  -> 15 - адрес возврата
		5120 >> 9 -> 10 адрес процедуры
		4)Subtract the immediate constant 16 from the stack pointer 
		5)Compare the actual parameter to the immediate constant 4 
			5124 >> 9 -> 10 -> инструкция сравнения.
			Actual параметр видимо то, что мы запушили с регистра -
			8188 >> 9 -> 15
		6)Jump if equal to 5152
			Инструкция 5128 >> 9 -> 10
			Адрес 5152 >> 9 -> 10
		Итого: 1 12 2 15 2 15 10 10 15 10 10
22. A computer whose processes have 1024 pages in their address spaces keeps its page tables in memory. The overhead required for reading a word from the page table is 5 nsec. To reduce this overhead, the computer has a TLB, which holds 32 (virtual page, physical page frame) pairs, and can do a lookup in 1 nsec. What hit rate is needed to reduce the mean overhead to 2 nsec?
		5\*p + 1\*(1 - p) =2
		p = 0.25 -> hitrate = 75%
23. The VAX was the dominant computer at university computer science departments dur ing most of the 1980s. The TLB on the VAX did not contain an R bit. Nevertheless, these supposedly intelligent people kept buying VAXes. Was this just due to their loy alty to the VAX’ predecessor, the PDP-11, or was there some other reason they put up with this for years?
		Есть алгоритмы замещения в TLB, которые не требуют R бита. Например просто замещать страницы рандомно, для 32 вхождений дает вполне приемлемую эффективность. Также я думаю, что это было сделано для стандартизации, или потому что плюсы VAX покрывали минусы.
24. Amachine has 48-bit virtual addresses and 32-bit physical addresses. Pages are 8 KB. Howmanyentries are needed for a single-level linear page table?
		2 ^ 48 / 2 ^ 13 = 2 ^ 35 
25. A computer with an 8-KB page, a 256-KB main memory, and a 64-GB virtual address space uses an inverted page table to implement its virtual memory. How big should the hash table be to ensure a mean hash chain length of less than 1? Assume that the hash table size is a power of two.
		Я вообще ничего не понимаю в криптографии, кроме RSA и DH.  Так что тут все по Дипсику. При этом я знаю, что размер инвертированной таблицы равен количеству физических кадров, а не виртуальной.
		Утверждается, что для того, чтобы цепочка коллизий - mean hash chain length - была меньше 1, то нужно чтобы хэш таблица была равна количеству физических кадров, то есть 256 / 8 = 32
26. A student in a compiler design course proposes to the professor a project of writing a compiler that will produce a list of page references that can be used to implement the optimal page replacement algorithm. Is this possible? Why or why not? Is there any thing that could be done to improve paging efficiency at run time?
		Даже с учетом того, что ОС может поменять поменять адрес начала программы и адрес кучи, из-за ASLR, компилятор все еще не знает полную информацию об адресах - динамической памяти на этом этапе не существует впринципе, а shared библиотеки динамически линкуются на этапе выполнения. Поэтому в общем случае это невозможно. +Порядок выполнения потоков генерируется ОС.
		Для ускорения во время рантайма компилятор может попробовать как-то структурировать код, чтобы то, что выполняется в текущий момент выполнялось на небольшом диапазоне страниц - но это очень сомнительно из-за большоого количества функций, которые используются постоянно в любой части кода и библиотек
27. Suppose that the virtual page reference stream contains repetitions of long sequences of page references followed occasionally by a random page reference. For example, the sequence: 0, 1, ... , 511, 431, 0, 1, ... , 511, 332, 0, 1, ... consists of repetitions of the sequence 0, 1, ... , 511 followed by a random reference to pages 431 and 332. (a) Why will the standard replacement algorithms (LRU, FIFO, clock) not be effective in handling this workload for a page allocation that is less than the sequence length? (b) If this program were allocated 500 page frames, describe a page replacement
		1. Это не эффективно, поскольку каждый раз та часть страниц, под которую не выделена память будет вызывать page fault. Когда они будут добавлять в память, другая страница будет выгружаться из памяти, а она нам понадобиться на следующем повторении последовательность
		2.  Страница 0-499 загрузятся в память. Далее оставшиеся страницы будут требовать замещения - страницы 0-12 будут выгружены, вместо них будут загружены 500-511 и 431/332.  Таким образом страницы, которые скоро понадобятся, выгружаются из памяти. В данном случае нужен алгоритм, который будет учитывать текущий циклический паттерн
28. If FIFO page replacement is used with four page frames and eight pages, how many page faults will occur with the reference string 0172327103 if the four frames are ini tially empty? Now repeat this problem for LRU.
		1. 3 заменит 0. 0 заменит 1 - 6 page fault
		2.  3 заменит 0. 0 заменит 3. 3 заменит 2 - 7 page fault
29. Consider the page sequence of Fig. 3-15(b). Suppose that the R bits for the pages B through A are 11011011, respectively. Which page will second chance remove?
		Страница D - она самая старая и на нее не ссылались, поэтому она будет выгружена с памяти.
30. A small computer on a smart card has four page frames. At the first clock tick, the R bits are 0111 (page 0 is 0, the rest are 1). At subsequent clock ticks, the values are  1011, 1010, 1101, 0010, 1010, 1100, and 0001. If the aging algorithm is used with an 8-bit counter, give the values of the four counters after the last tick.

|     | 1   | 2   | 3   | 4    | 5     | 6      | 7       | 8        |     |
| --- | --- | --- | --- | ---- | ----- | ------ | ------- | -------- | --- |
| 0   | 0   | 10  | 110 | 1110 | 01110 | 101110 | 1101110 | 01101110 |     |
| 1   | 1   | 01  | 001 | 1001 | 01001 | 001001 | 1001001 | 01001001 |     |
| 2   | 1   | 11  | 111 | 0111 | 10111 | 110111 | 0110111 | 00110111 |     |
| 3   | 1   | 11  | 011 | 1011 | 01011 | 001011 | 0001011 | 10001011 |     |
31. Give a simple example of a page reference sequence where the first page selected for replacement will be different for the clock and LRU page replacement algorithms. Assume that a process is allocated 3=three frames, and the reference string contains page numbers from the set 0, 1, 2, 3.
32. A student has claimed that ‘‘in the abstract, the basic page replacement algorithms (FIFO, LRU, optimal) are identical except for the attribute used for selecting the page to be replaced.’’ (a) What is that attribute for the FIFO algorithm? LRU algorithm? Optimal algorithm? (b) Give the generic algorithm for these page replacement algorithms.
		a) насколько давно страница был загружен в память - FIFO, насколько давно к странице обращались - LRU,  насколько близка следующая инструкция программы на этой странице - optimal
		b)Грубо говоря выбрать максимальное значение параметра из всех -> и выгрузить эту страницц
33. How long does it take to load a 64-KB program from a disk whose average seek time is 5 msec, whose rotation time is 5 msec, and whose tracks hold 1 MB (a) for a 2-KB page size? (b) for a 4-KB page size? The pages are spread randomly around the disk and the number of cylinders is so large that the chance of two pages being on the same cylinder is negligible.
			seek time - головка встает на нужный диск и дорожку - 5мс
			rotation time - время за которое головка прокручивается над диском. Тогда скорость чтения равна 1\*1024 / 5 = 204.8 KB/мс. Нейронка говорит, что мы берем среднее время вращения, то есть время, пока головка не докрутится до нужной секции на дорожке - оно равно 5 / 2 = 2.5 Общее время для каждой страница 2КБ- 5мс + 2.5 + 2/204.8 =7.5 + 0.01 = 7.51. Общее время для файла - 7.51 \* 32  = 240.32.  Общее время для каждой страница 4КБ- 5мс + 2.5 + 4/204.8 =7.5 + 0.02 = 7.52. Общее время для файла - 7.52 \* 16  = 120.32
34. Consider the FIFO page replacement algorithm and the following reference string: 45 When the number of page frames increases from three to four, does the number of page faults go down, stay the same, or go up? Explain your answer.
		1 -> 2 -> 3  
		2 -> 3 -> 4
		3 -> 4 -> 1
		4 - > 1 -> 2
		1 -> 2 -> 5
		2 -> 5 -> 3
		5 -> 3 -> 4
		9 страничных промахов
		1 -> 2 -> 3 -> 4
		2 -> 3 -> 4 -> 5
		3 -> 4 -> 5 -> 1
		4 -> 5 -> 1 -> 2
		5 -> 1 -> 2 -> 3
		1 -> 2 -> 3 -> 4
		2 -> 3 -> 4 -> 5
		10 страничных промахов
		Количество уменьшилось

35. A computer has four page frames. The time of loading, time of last access, and the R and Mbits for each page are as shown below (the times are in clock ticks): 1 (a) Which page will NRU replace? (b) Which page will FIFO replace? (c) Which page will LRU replace? 1 (d) Which page will second chance replace?
	 ![[Pasted image 20260111202411.png]]
		a)  2
		b) 3
		c) 1
		d) 2
36. Suppose that two processes A and B share a page that is not in memory. If process A faults on the shared page, the page table entry for process A must be updated once the page is read into memory. (a) Under what conditions should the page table update for process B be delayed even though the handling of process A’s page fault will bring the shared page into mem ory? Explain. (b) What is the potential cost of delaying the page table update?
		1) Page fault - критическая ситуация, когда все должно происходить очень быстро. Имеет смысл отложить обновление таблицы процесса B, если он не выполняется, для ускорения обработки page fault.
		2) Если процесс B обратится к разделяемой странице раньше, чем его страница обновится, то произойдет minor page fault - когда страница в виртуальном адресном пространстве другого процесса.
37. 37. Consider the following two-dimensional array:
int X\[64]\[64];
Suppose that a system has four page frames and each frame is 128 words (an integer
occupies one word). Programs that manipulate the X array fit into exactly one page
and always occupy page 0. The data are swapped in and out of the other three frames.
The X array is stored in row-major order (i.e., X\[0]\[1] follows X\[0]\[0] in memory).
Which of the two code fragments shown below will generate the lowest number of
page faults? Explain and compute the total number of page faults.
Fragment A
	for (int j = 0; j < 64; j++)
		for (int i = 0; i < 64; i++) X\[i]\[j] = 0;
	Мы будет прыгать со страницы на страницу. Поскольку страничных кадров 4, а страниц 32, то каждая итерация внутреннего цикла будет вызывать страничный промах -> 32 \* 64 = 2048
Fragment B
	for (int i = 0; i < 64; i++)
		for (int j = 0; j < 64; j++) X\[i]\[j] = 0;
			Если условно X\[0]\[0] - адрес 0, а X\[0]\[1] - 1, то фактически мы постепенно идем как бы вверх по памяти. Раз страничный кадр вмещает 128 интов, то 64 / 2 = 32 -> столько страничных промахов.
Очевидно, что второй код лучше
38. One of the first timesharing machines, the DEC PDP-1, had a (core) memory of **4K 18-bit words**. It held one process at a time in its memory. When the scheduler decided to run another process, the process in memory was written to a paging drum, with **4K 18-bit** words around the circumference of the drum. The drum could start writing (or reading) at any word, rather than only at word 0. Why do you suppose this drum was chosen?
		Отличие paging drum от устройства современного HDD в том, что головки фиксированы - не надо наводить их на каждую дорожку. Тогда seek time пропадает -> остается только lattency на прокрутку, до нужного места. Очевидно, что мы не хотим ждать, пока головка докрутится до 0, потом докручивать ее до нужного сектора и только потом читать. Поэтому в PDP-1 дорожка не возвращалась к 0, а начинала читать с любого слова.
39. A computer provides each process with 65,536 bytes of address space divided into pages of 4096 bytes each. A particular program has a text size of 32,768 bytes, a data size of 16,386 bytes, and a stack size of 15,870 bytes. Will this program fit in the machine’s address space? Suppose that instead of 4096 bytes, the page size were 512 bytes, would it then fit? Each page must contain either text, data, or stack, not a mix ture of two or three of them.
			Всего страниц - 16 в памяти
			Текст программы займет 8 страниц
			Данные займут - ceil(4.0004) = 5 страниц
			Стек - ceil(3.87) = 4 страницы
			Итого - 17 страниц -> не влезет в память
			Всего страниц - 128 в памяти
			Текст программы займет 64 страниц
			Данные займут - ceil(32.003) = 33 страниц
			Стек - ceil(30.99) = 31 страницы
			Итого - 128 страниц ->  влезет в память
40. Can a page be in two working sets at the same time? Explain.
	Да. Самый очевидный пример, страницы shared библиотек в рабочем наборе 2 процессов. 
	Если говорить об одном процессе.  Нельзя
41. If a page is shared between two processes, is it possible that the page is read-only for one process and read-write for the other? Why or why not?
		Механически да, потому что protection-биты устанавливаются ОС в таблице страниц каждого процесса.  Но при этом нейронка говорит, что так нельзя делать, потому что:  нужно инвалидировать страницу с правами в TLB для второго процесса - на многопоточных системах это достаточно долгая операция
42. It has been observed that the number of instructions executed between page faults is directly proportional to the number of page frames allocated to a program. If the avail able memory is doubled, the mean interval between page faults is also doubled. Sup pose that a normal instruction takes 1 microsec, but if a page fault occurs, it takes 2001 µsec (i.e., 2 msec) to handle the fault. If a program takes 60 sec to run, during which time it gets 15,000 page faults, how long would it take to run if twice as much memory were available?
			15000 \* 2.001 / 1000 = 30.015sec - время всех страничных промахов
			60 / 30.015 = 1.999 ~ 2 периодичность
			2 \* 2 = 4 - c удвоенной памятью в 2 раза реже
			60 \ 4 =15sec займут page fault
			ans = 60 - (30.015 - 15) ~ 45sec
43. Agroup of operating system designers for the Frugal Computer Companyare thinking about ways to reduce the amount of backing store needed in their new operating sys tem. The project manager has just suggested not bothering to save the program text in the swap area at all, but just page it in directly from the binary file whenever it is need ed. Under what conditions, if any, does this idea work for the program text? Under what conditions, if any, does it work for the data?
			1) Для текста программы наверное должны быть гарантии, что никто не удалит бинарник с диска и он будет доступен. А так он не меняется и смысла swap area забивать им нет, лучшее просто сослаться на файл, который и так есть на диске.
			2) Data segment не статичен. Тем не менее, мы можем так сделать, но используя memory mapped подход, когда мы напрямую ссылаемся на память. Нужно либо сразу записывать изменения в файл, либо использовать copy-on-write
44. Amachine-language instruction to load a 32-bit word into a register contains the 32-bit address of the word to be loaded. What is the maximum number of page faults this instruction can cause?
		Сама инструкция может храниться на 2 страницах и машинное слово на 2 страницах -> итого 4 страницы
45. Explain the difference between internal fragmentation and external fragmentation. Which one occurs in paging systems?Which one occurs in systems using pure seg mentation?
		internal fragmentation - процесс не полностью заполняет страницу, или же memory chunk выделенный части программы не полностью заполнен. Происходит при paging - почти каждая страница не полностью заполнена
		external fragmentation - процесс выгружается из памяти, образуется дырка. Это и есть external fragmentation. Происходит при использовании сегментации.
 46. When segmentation and paging are both being used, as in MULTICS, first the segment descriptor must be looked up, then the page descriptor.Does the TLB also work this way, with twolev els of lookup?
		 Цитата из Танненбаума: An address in MULTICS consisted of two parts: the segment and the address within the segment. The address within the segment was further divided into a page number and a word within the page, as shown in Fig. 3-35.t

		Если ОС знает и номер сегмента и виртуальный адрес внутри сегмента, то мы можем напрямую обратится в TLB используя {segmentNumber, virtual address} пару ключей. Да, мы используем ключ из двух значений, но не используем 2 раздельных TLB, так что я думаю можно сказать, что это одноуровневый подход
	47. ![[Pasted image 20260115211528.png]]
50.Plot a histogram and calculate the mean and median of the sizes of executable binary files on a computer to which you have access. On a Windows system, look at all .exe and .dll files; on a UNIX system look at all executable files in /bin, /usr/bin, and CHAP. 3 PROBLEMS 257 /local/bin that are not scripts (or use the file utility to find all executables). Determine the optimal page size for this computer just considering the code (not data). Consider internal fragmentation and page table size, making some reasonable assumption about the size of a page table entry. Assume that all programs are equally likely to be run and thus should be weighted equally.
Вод код на питоне для гистограммы и 
```c
import pathlib
import os
import matplotlib.pyplot as plt
import fnmatch
from statistics import *
allExeFiles = []
allSmallerThan64 = 0
allCloseTo64 = 0
allExE = 0

def countExe(disk):
    delta = 15
    global allCloseTo64,allSmallerThan64,allExE
    for dirpath, dirnames, files in os.walk(f"{disk}:/", topdown=True):
        for file_name in files:
            if file_name.endswith(".exe"):
                size = os.stat(dirpath + '/' + file_name).st_size / 1024 
                if size < 64 - delta: 
                    allSmallerThan64 += 1
                if size < 64 and size > 64 - delta:
                    allCloseTo64 += 1
                allExE += 1
                allExeFiles.append(size)
countExe("D")
countExe("C")
countExe("E")
print(mean(allExeFiles))
print(median(allExeFiles))
print(min(allExeFiles))
print(max(allExeFiles))
print(allExE, allSmallerThan64, allCloseTo64)
print(sum(allExeFiles))
#print(allExeFiles)
plt.hist(allExeFiles, bins=200)
plt.show()
```
Среднее значение - 1936КБ, медиана - 86. Большая часть exe файлов на моем ПК размером меньше 1МБ -> оптимальнее брать медиану. Тогда размер страницы ~ 80КБ, но лучше брать степень двойки - 64КБ. 
Internal Fragmentation - путем подбора размера страниц лучше всего подойдут страницы по 64КБ с таким выводом - 7370 2621 431.  
Виртуальное адресное пространство должно быть больше самого большого файла - в моем случае 692290КБ -676МБ. Тогда ВАП, учитывая то, что текст программы статичен должно быть равно 1ГБ. 1024 / 64 - 16 вхождений в каждую таблице страниц
На диаграмме можно заметить, что большая часть страниц маленькая - меньше 1МБ. Это связано с тем, что у меня в системе много exe утилит - mingw, wsl, cygwin, mysys экзешные файлы. Их очень много, но весят они при этом мало.

51. Write a program that simulates a paging system using the aging algorithm. The number of page frames is a parameter. The sequence of page references should be read from a file. For a given input file, plot the number of page faults per 1000 memory references as a function of the number of page frames available.
с++ код для логики
```c
	#include <iostream>
#include <thread>
#include <chrono>
#include <semaphore>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include "mailboxapi.h"
#include <string>
#include <set>
#include <fstream>
#include <map>
#include <cinttypes>
#include <algorithm>
#include <atomic>

struct page {
    uint8_t bits;
    bool R;
    int pageNum;
};

bool comp(page &p1, page &p2) {
    return p1.bits < p2.bits;
}
int n; // индекс страницы на замещение
std::vector<page>pages;
std::binary_semaphore sem{1};
int pageFaults = 0;
std::atomic<bool>flag{false};
//обновляет страницы учитывая R биты + фоново вычисляет минимальную страницу.
void makeAging() {
    sem.acquire();
        int minNum = 1e9;
        for (int i = 0; i < pages.size(); ++i) {
           page* curPage = &pages[i];
           curPage->bits = curPage->bits >> 1;
           if (curPage->R == 1)  curPage->bits = (curPage->bits | (1 << 7));
           curPage->R = 0;
        }
    sem.release();
}

//поток обновления состояния
void aging(int n) {
    // раз в 15 мс обновляем состояния с учетом R битов
    while (!flag) {
        makeAging();
        std::this_thread::sleep_for(std::chrono::milliseconds(15)); //имитация прерываний по таймеру
    }
}

void PFhandler(int pageNum) {
    //обычный mr, ставим R бит в 1
    sem.acquire();
    for (int i = 0 ; i < pages.size(); ++i) {
        if (pageNum == pages[i].pageNum) {
            pages[i].R = 1;
            sem.release();
            return;
        }
    }
    if (pages.size() < n) {
        pages.push_back({0, 1, pageNum});
        pageFaults += 1;
        sem.release();
        return;
    }
    //page fault
    int candRep  = std::min_element(pages.begin(), pages.end(), comp) - pages.begin();
    pages[candRep] = {0, 1, pageNum};// заменяем уже заранее подготовленную страницу;
    pageFaults += 1;
    sem.release();
}

int main() {
    int pageNum;
    std::cin >> n;
    std::ifstream file("file.txt");
    std::thread agingThread(aging, n);
    while (file >> pageNum) {
        PFhandler(pageNum);
    }
    flag = true;
    agingThread.join();
    std::cout << pageFaults << std::endl;
    return 0;
}
```
python-скрипты для заполнения и для построения диаграммы.
```c
file = open("C:/Users/0987a/OneDrive/Рабочий стол/iris/message passing/file.txt", "w")
for i in range(1000):
    page = random.randint(1, 50)
    file.write(str(page) + "\n")
    
file = open("C:/Users/0987a/OneDrive/Рабочий стол/iris/message passing/dFile.txt", "r")
x = []
y = []
for l in file:
    a = list(map(int,l.split(' ')))
    x.append(a[0])
    y.append(a[1])
plt.plot(x, y)
plt.show()
```
![[Figure_1.png]]
52. Write a program that simulates a toy paging system that uses the WSClock algorithm. The system is a toy in that we will assume there are no write references (not very real istic), and process termination and creation are ignored (eternal life). The inputs are: • The reclamation age threshold • The clock interrupt interval expressed as number of memory references • Afile containing the sequence of page references (a) Describe the basic data structures and algorithms in your implementation. (b) Show that your simulation behaves as expected for a simple (but nontrivial) input example. (c) Plot the number of page faults and working set size per 1000 memory references. (d) Explain what is needed to extend the program to handle a page reference stream that also includes writes.

Пожалуй что самое сложное задание которые я делал. В первую очередь, потому что нейронки не знают какая у WSClock реализация на самом деле. Можно искать кандидата фоново, можно в момень pageFault. Можно в момент pageFault двигать hand, а можно просто бегать по индексам. Я написал что-то такое, чуть чуть юзнул гпт, чтобы пофиксить висячие указатели. Получилось вроде нечто рабочее, хотя оценка от обоих нейронок низкая, потому что они не согласны с реализацией.
```c
#include <iostream>
#include <vector>
#include <fstream>

struct page {
    int R;
    int MFtime;
    int pageNum;
    int M;
};

struct timer {
    std::vector<page> vec;
    int hand;
};

timer pages;
int virtualTimer = 0;
const int pagesForWSClock = 10;

void diskOperation() {}

void WSClock(int* reclamationAge) {
    int it = 0;
    while (it < pagesForWSClock && !pages.vec.empty()) {
        page& curEl = pages.vec[pages.hand];

        if (curEl.M == 1 && curEl.R == 0) {
            if (virtualTimer - curEl.MFtime > *reclamationAge) {
                diskOperation();
                curEl.M = 0;
            }
        }

        curEl.R = 0;
        pages.hand = (pages.hand + 1) % pages.vec.size();
        it++;
    }
}

int PR(int* pageNum, int* reclamationAge, int* pageFrames) {
    for (auto& p : pages.vec) {
        if (p.pageNum == *pageNum) {
            p.R = 1;
            p.MFtime = virtualTimer;
            return 0;
        }
    }

    if ((int)pages.vec.size() < *pageFrames) {
        pages.vec.push_back({1, virtualTimer, *pageNum, 0});
        if (pages.vec.size() == 1) pages.hand = 0;
        return 1;
    }

    int spared = -1;

    for (int i = 0; i < pages.vec.size(); i++) {
        auto& p = pages.vec[i];
        if (p.R == 0 && p.M == 0 && virtualTimer - p.MFtime > *reclamationAge) {
            p = {1, virtualTimer, *pageNum, 0};
            return 1;
        }
        if (p.M == 0 && spared == -1) spared = i;
    }

    if (spared == -1) spared = pages.hand;

    pages.vec[spared] = {1, virtualTimer, *pageNum, 0};
    pages.hand = (spared + 1) % pages.vec.size();

    return 1;
}

int main() {
    int reclamationAge = 10, clockInterrupt = 4;

    for (int pageFrames = 5; pageFrames < 30; pageFrames++) {
        pages.vec.clear();
        pages.hand = 0;
        virtualTimer = 0;

        std::ifstream file("file.txt");
        std::ofstream file1("dFile.txt", std::ios::app);

        int currentMF, counter = 0, pageFaults = 0;

        while (file >> currentMF) {
            virtualTimer++;
            counter++;

            if (counter == clockInterrupt) {
                WSClock(&reclamationAge);
                counter = 0;
            }

            pageFaults += PR(&currentMF, &reclamationAge, &pageFrames);
        }

        file1 << pageFrames << " " << pageFaults << '\n';
    }
}

```
Скрипт генерации рабочего набора
```c
import random
import matplotlib.pyplot as plt
file = open("C:/Users/0987a/OneDrive/Рабочий стол/iris/message passing/file.txt", "w")
#доустим страницы рабочего набора в 10 раз чаще чем не в рабочем наборе
#раочий набор размера n
#x - вероятность обычной страницы
#всего 100 страниц
for n in range(1, 100):
    #10 * n * x + (100 - n) * x = 1
    x = 1 / (9*n + 100)
    chances = []
    for i in range(100):
        if i < n: chances.append(10 * x)
        else: chances.append(x)
    #создали  массив с учетом рабочего набора
    result = random.choices(range(0,100), weights=chances, k=1000)
    file.write(str(n) + '\n')
    for i in result: file.write(str(i) +'\n')
```
График. По хорошему он должен быть чисто линейный. Это связано с тем, что при маленьком рабочем наборе у меня остается вероятность в 10 раз больше чем у других страниц. Можно переделать, но смысла не сильно много поскольку рабочий набор не бывает размером в 1 страницу
![[Figure_1 2.png]]

53. Write a program that demonstrates the effect of TLB misses on the effective memory access time by measuring the per-access time it takes to stride through a large array. (a) Explain the main concepts behind the program, and describe what you expect the output to show for some practical virtual memory architecture. (b) Run the program on some computer and explain how well the data fit your expecta tions. (c) Repeat part (b) but for an older com
54.  a) Суть программы в том, чтобы показать эффект TLB misses. В первой части кода я просто бегу по страницам. Таким образом TLB miss происходит каждый раз, когда начинается новая страница. Во втором коде TLB miss происходит постоянно - код должен выполняться дольше
```c
#include <iostream>
#include <vector>
#include <chrono>

const int size = 1000000;
int a[size];

int main() {
    std::fill(a, a + size - 1, 0);
    int pageSize = 1024;
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0 ; i < size; ++i)   a[i]++;
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = end - start;
    std::cout << duration.count() << std::endl;
    auto start1 = std::chrono::high_resolution_clock::now();
    for (int j = 0 ; j < pageSize; ++j) {
        for (int i = 0 ; i < (size - pageSize); i+=pageSize) {
            a[i + j]++;
        }
    }
    auto end1 = std::chrono::high_resolution_clock::now();
    auto duration1 = end1 - start1;
    std::cout << duration1.count() << std::endl;
    return 0;
}
//питон скрипт
import random
import matplotlib.pyplot as plt
file = open("C:/Users/0987a/OneDrive/Рабочий стол/iris/message passing/file.txt", "w")

#допустим страницы рабочего набора в 10 раз чаще чем не в рабочем наборе
#рабочий набор размера n
#x - вероятность обычной страницы
#всего 100 страниц
for n in range(1, 100):
    #10 * n * x + (100 - n) * x = 1
    x = 1 / (9*n + 100)
    chances = []
    for i in range(100):
        if i < n: chances.append(10 * x)
        else: chances.append(x)
    #создали  массив с учетом рабочего набора
    result = random.choices(range(0,100), weights=chances, k=1000)
    file.write(str(n) + '\n')
    for i in result: file.write(str(i) +'\n')
скрипт для генерации рабочего набора
```
b) Запуск показал огромное различие в производительности -	1874400 для первого и 
8772300 для второго - в 4.5 раза. Так происходит, потому что на каждой итерации я обращаюсь к новой странице
с)нет доступа к компа с другой архитектурой


55. Write a program that will demonstrate the difference between using a local page replacement policy and a global one for the simple case of two processes. You will need a routine that can generate a page reference string based on a statistical model. This model has N states numbered from 0 to N 1 representing each of the possible page references and a probability pi associated with each state i representing the chance that the next reference is to the same page. Otherwise, the next page reference will be one of the other pages with equal probability. (a) Demonstrate that the page reference string-generation routine behaves properly for some small N. (b) Compute the page fault rate for a small example in which there is one process and a fixed number of page frames. Explain why the behavior is correct. (c) Repeat part (b) with two processes with independent page reference sequences and twice as many page frames as in part (b). (d) Reroach.peat part (but using a global policy instead of a local one. Also, contrast the per-process page fault rate with that of the local policy app
Ответ:
```c
//Код рутины
length = 1000
file = open("C:/Users/0987a/OneDrive/Рабочий стол/iris/message passing/file.txt", "w")
n = int(input()) #1-n все возможные страницы
p = []
for el in range(n):  p.append(random.random())
referenceString = ''
print(p)

el = int(random.randint(0, n - 1)) #задали первый элемент, p[el] - нужная
referenceString += str(el) + " "

for i in range(1, length):
    allProbabilities = (1 - p[el]) /(n - 1) #распределяем поровну вероятности между остальынм
    chances = []
    for i in range(n):
        if (i == el): chances.append(p[el])
        else: chances.append(allProbabilities)
    result = random.choices(range(0,n), weights=chances, k=1)
    el = result[0]
    referenceString+= (str(el) + " ")
file.write(referenceString)
```
(a) Для n = 3 и length = 5, вывелось в первый раз - 0 2 0 1 0, во второй раз - 2 2 2 2 1, это показывает что строка действительно генерируется рандомно.
(b) В коде много костылей, но от этого он не перестает  быть рабочим. Все обьяснения кода есть в комментариях. Я много ломал его на пограничных случаях - все работает. На больших данных никаких ошибок не вызывает
```c
#include <iostream>
#include <vector>
#include <fstream>
const int PageFrames = 4;

struct leaf {
    int value = -1000;
    leaf* nextValue = nullptr;
};

int pageFaults = 0;
leaf* head = new leaf;
leaf* back = new leaf;

void LRU(leaf*& node, int param, leaf* object = nullptr) {
    if (param == 0) {//param == 0 -> обработка page hit;
        if (back == node) return; //веришна итак последняя - ничего делать не надо
        back->nextValue = node->nextValue; // перетащили вершину между двумя в конец линкед листа
        node->nextValue = node->nextValue->nextValue;
        back = back->nextValue;
        back->nextValue = nullptr;
    }
    if (param == 1) {
        back->nextValue = object;
        back = back->nextValue;
        leaf* temp = head;
        head = head->nextValue;
        delete temp;
    }
    if (param == 2) {
        if (head->nextValue == nullptr) head->nextValue = object;
        back->nextValue = object;
        back = back->nextValue;
    }
}

int PR(int* page) {

    int currentDeep = 0; // вспомогательная переменная;
    bool onlyHead = false; // вспомогательная переменная;
    // список неиницилизирован
    if (head->value == -1000) {
        head->value = *page;
        back->value = *page;
        std::cout << head << " " << back << std::endl;
        return 1;
    }
    //если есть всего 1 страничный кадр - пограничный случай
    if (PageFrames == 1) {
        if (head->value == *page) return 0;
        else {
            head->value = *page;
            return 1;
        }
    }
    //если 1 страница и page hit
    
    if (head->value == back->value && *page == head->value) { //костыль
        std::cout << "here" << std::endl;
        return 0;
    }

    //page hit
    leaf* node = nullptr;
    node = head;
   
   
    if (head->value == *page) { //corner case
        back->nextValue = head;
        back = back->nextValue;
        head = head->nextValue;
        node->nextValue = nullptr;
        return 0;
    }

    while (true) {
        currentDeep += 1;
        if (node->nextValue != nullptr && node->nextValue->value == *page) {
            LRU(node, 0);
            return 0;
        }
        if (node->nextValue == nullptr) break;
        node = node->nextValue;
    }


    //page fault, но не все страничные фрэймы заняты

    leaf* objectPtr = new leaf;
    *objectPtr = { *page, nullptr };

    if (currentDeep < PageFrames) {
        LRU(node, 2, objectPtr);
        return 1;
    }
    //page fault
    LRU(node, 1, objectPtr);
    return 1;
}

int main() {
    int linkedListSize = 0;
    int page;
    *head = { -1000, nullptr };
    *back = { -1000, nullptr };
    std::ifstream file("secondsequence.txt");
    while (file >> page) {
        pageFaults += PR(&page);
        leaf* node = head;
        while (node) {
            std::cout << node->value << " ";
            node = node->nextValue;
        }
        std::cout << std::endl;
    }
    //memory freeing
    while (head) {
        leaf* temp = head;
        head = head->nextValue;
        delete temp;
    }
    std::cout << pageFaults;
}
```
(c) Я 2 раза запустил программу на разных последовательнастях и просто просуммировал. Получилось 151 + 336  = 487 страничных промахов, при N = 100, pageFrames = 40;
(d) Нужно переписать код реализации linked листа в array pool в shared памяти -> на raw указателях ничего работать не будет
```c
#include <iostream>
#include <thread>
#include <chrono>
#include <semaphore>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string>
#include <set>
#include <fstream>
#include <map>
#include <cinttypes>
#include <algorithm>
#include <atomic>
#define ll long long
const int MaxSize = 2000;
const int PageFrames = 4;


struct leaf {
    int page; // номер страницы
    int next; // по какому индексу следующий элемент;
};

struct DList { // порядок в shared memory гарантируется компилятором
    leaf arrayPool[MaxSize];
    int head; // индекс начала linked lista
    int back; // индекс конца linked lista
    int size;
    ll pf = 0;
};

DList* dlist;

void output() {
    leaf* node = &(dlist->arrayPool[dlist->head]);
    std::cout << "1 ";
    while (true) {
        std::cout << " { " << node->page << " " << node->next << " } ";
        if (node->next == -1) break;
        node = &dlist->arrayPool[node->next];
        //std::this_thread::sleep_for(std::chrono::milliseconds(15));
    }
    std::cout << std::endl;
}

void prefill(int page) {
    dlist->arrayPool[dlist->back].next = dlist->back + 1;
    dlist->arrayPool[dlist->back + 1].page = page;
    dlist->arrayPool[dlist->back + 1].next = -1;
    dlist->back++;
    dlist->size++;
}

void init(int page) {
    dlist->head = 0;
    dlist->back = 0;
    dlist->size = 1;
    dlist->arrayPool[dlist->head].page = page;
    dlist->arrayPool[dlist->head].next = -1;
}

void printArray() {
    for (int i = 0 ; i < PageFrames; ++i) std::cout << dlist->arrayPool[i].page << " | " << dlist->arrayPool[i].next << " }";
    std::cout << std::endl;
}
int pageHit(int page) {
    leaf* node = &(dlist->arrayPool[dlist->head]);
    while (true) {
        if (node->next == -1) break;
        leaf* equalNode = &(dlist->arrayPool[node->next]);
        bool isHead = (dlist->arrayPool[dlist->head].page == page);
        bool equalPage = (equalNode->page == page);

        if (isHead) { //corner case - голова совпала с листом, двигаем голову
            dlist->arrayPool[dlist->back].next = dlist->head;
            dlist->back = dlist->head;
            dlist->head = node->next;
            node->next = -1;
            return 0;
        }
        if (equalPage) {
            if (dlist->back == node->next) return 0;
            dlist->arrayPool[dlist->back].next = node->next; //привязали равную вершину за конец
            dlist->back = node->next; //конец на этой вершин
            node->next = equalNode->next; // привязали через одну
            equalNode->next = -1; //отвязали равную вершину
            return 0;
        }
        node = &dlist->arrayPool[node->next];
    }
    return 1;
}

int pageFault(int page) {
    dlist->arrayPool[dlist->back].next = dlist->head;
    dlist->back = dlist->head;
    dlist->head = dlist->arrayPool[dlist->head].next;
    dlist->arrayPool[dlist->back].next = -1;
    dlist->arrayPool[dlist->back].page = page;
    return 1;
}
int PR(int page) {

    if (dlist->head == -1) { //инициализация
        init(page);
        return 1;
    }

    if (dlist->size < PageFrames) {
        prefill(page); // заполняем весь linked list
        return 1;
    }

    //page hit;
    int result = pageHit(page);
    if (result == 0) return result;

    //page fault
    return pageFault(page);
}

void Programm(std::string filename, sem_t *sem) {
    int page;
    std::ifstream file(filename);
    while (file >> page) {
        sem_wait(sem);
        dlist->pf += PR(page);
        sem_post(sem);
    }
}

int main() {
    //создать второй процесс, подключить к shared памяти, сделать считывание со второго файла+всю логику pr, синхронизировать все.
    char* name = "/sharedMemory";
    int shm =  shm_open(name, O_CREAT | O_RDWR, S_IRWXO | S_IRWXG | S_IRWXU);
    if (shm == -1) std::cerr << "error in creating shared memory";
    int isOk = ftruncate(shm, sizeof(DList));
    if (isOk == -1) std::cerr << "error in allocating memory";
    dlist = (DList*) mmap(nullptr, sizeof(DList), PROT_WRITE | PROT_READ, MAP_SHARED, shm, 0);
    dlist->head = -1;
    char* semaphoreName = "/myName";
    sem_t *sem = sem_open(semaphoreName, O_CREAT, 0666, 1);
    pid_t result = fork();
    if (result < 0) {
        std::cerr << "error in creating process";
    }
    else if (result == 0) { //second process code
        Programm("secondsequence.txt", sem);
        std::cout << "Second First" << dlist->pf << std::endl;
        _exit(0);
    }
    Programm("firstsequence.txt", sem);
   // УДАЛИТЬ shared memory объект
    std::cout <<  "First first " << dlist->pf << std::endl;
    //2 cout -> из-за непонятки какой процесс закончится первый тяжеловато получить ответ
    //поэтому ответ просто максимум из 2 cout;
    sem_close(sem);
    sem_unlink(semaphoreName);
    munmap(dlist, sizeof(DList));      // отвязать от адресного пространства
    close(shm);              // закрыть дескриптор
    shm_unlink(name);

}
```
Получилось 494 -> примерно то же самое. Однако затраты на то, чтобы синхронизировать shared память в настоящих системах я думаю будут ощутимы.


55. Write a program that can be used to compare the effectiveness of adding a tag field to TLB entries when control is toggled between two programs. The tag field is used to effectively label each entry with the process id. Note that a nontagged TLB can be sim ulated by requiring that all TLB entries have the same tag at any one time. The inputs will be: • The number of TLB entries available • The clock interrupt interval expressed as number of memory references • Afile containing a sequence of (process, page references) entries • The cost to update one TLB entry (a) Describe the basic data structures and algorithms in your implementation. b) Show that your simulation behaves as expected for a simple (but nontrivial) input example. (c) Plot the number of TLB updates per 1000 references.
a)хэш таблица + рандомное заменение
b)работает
с)Tagged TLB - 8060 TLB FAULT - без учета рабочего набора
```c
#include <iostream>
#include <vector>
#include <map>
#include <fstream>


int TLBsize, clockInterrupt, cost, page, counter = 0, processID = 0, costSum = 0;
std::map<std::pair<int,int>, int> TLB;
std::vector<std::pair<int,int>> keys;

void output() {
    std::cout << "TLB size" << TLB.size() << std::endl;
    std::cout << "Page " << page << std::endl;
    std::cout << "Process ID " << processID << std::endl;
    for (auto [key, value] : TLB) {
        std::cout << key.first << " " << key.second << " " << value << std::endl;
    }
    std::cout << std::endl;
}
void PR() {
    bool isValid;
    if (TLB.size() < TLBsize && TLB.find({processID, page}) == TLB.end()) { // TLB не полностью заполнен
        TLB[{processID, page}] = processID; //буду класть processId, просто что бы что то класть, в целом это неважно
        keys.push_back({processID, page});
        costSum += cost;
        return;
    }

    if (TLB.find({processID, page}) != TLB.end()) return;  //страница найдена в TLB

    //TLB fault - Выбираем рандомную страницц
    int randomKey = rand() % keys.size();
    std::pair<int,int> currentPage = keys[randomKey];
    TLB.erase(currentPage); // удалили рандомную страницу

    keys[randomKey] = {processID, page};
    TLB[{processID, page}] = processID;
    costSum += cost;

}

int main() {

    std::cin >> TLBsize >> clockInterrupt >> cost;
    std::ifstream file("firstsequence.txt");
    std::ofstream file1("dFile.txt");
    int pr;
    int curSum = 0;
    int allSum = 0;
    while (file >> page) {
        counter++;
        if (counter % clockInterrupt == 0) {
            processID = !processID;
        }
        PR();
        if (counter % 1000 == 0) {
            curSum = costSum - allSum;
            allSum = costSum;
            std::cout << costSum << " " << curSum << std::endl;
            file1 << curSum << " ";
        }

    }
    std::cout << costSum << std::endl;
    return 0;
}


```
![[Pasted image 20260124132218.png]]

Для UNTAGGED TLB - 8016 фолтов
![[Pasted image 20260124031338.png]]
Впринципе то же самое)