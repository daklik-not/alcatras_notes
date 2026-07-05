1. What are the two main functions of an operating system?
		У ОС есть у функции: она должна распоряжаться ресурсами аппартного обеспечения и предоставлять программному обеспечению абстракции для работы с аппаратным. Например с помощью ОС передается информация, которая необходима для его вычислений. Для второго:  например, когда требуется прочитать какую-то информацию, ПО не заботится о  том, в каком блоке памяти на диске он лежит, оно работает с абстракцией - файлами и уже потом ОС понимает где именно лежит информация, записанная на этом файле.
2. What is multiprogramming?
		Мультипрограммирование, простыми словами говоря, это когда процессор очень быстро меняется между процессами и создается впечатление, что таким образом достигается истинный параллелизм. Именно ОС обеспечивает мультипрограммирование, решает приоритет процессов их время выполнения.
	Что не написал: изначально мультипрограммирование предполагает то, чтобы 1 процесс не простаивал, пока другой ждет чего-то.
3. In Sec. 1.4, nine different types of operating systems are described. Give a list of pos sible applications for each of these systems (at least one for each of the operating sys tems types). 
		PC systems - любое десктопное приложение, пусть например мессенджер.
		Real-time systems - программа конвейера на сталелитейном заводе.
		Embedded systems - программа калькулятора, совершающая вычисления(калькулятора как отдельное устройство)
		Mainframes - программа, следящая за всеми переводами, которые делают пользователи банка.
		Server systems - DNS сервер
		Systems for handhold devices - любое андроид приложение, например, мессенджер.
		Что забыл: Smart Card OS - например приложение, которое ловит сигнал с вышки сотовой связи и обрабатывает его.
		Остальных двух у меня просто нет в заметках, не понятно, что автор имел в виду.
4. To use cache memory, main memory is divided into cache lines, typically 32 or 64 bytes long. An entire cache line is cached at once. What is the advantage of caching an entire line instead of a single byte or word at a time? 
		Ответ вообще не засчитан, тем не менее я вообще не понимаю как я должен был до него догадаться. Кэш-линия использует принцип пространственной локальности. Ее смысл в том, что часто данные, к которым часто обращаются лежат рядом в памяти. Наример обработка массива - данные лежат рядом. Потом, следующая проблема в загрузке памяти из RAM. Загрузит 64 байтную кэш-линию не сильно больше затратнее чем 64 битное слово.
5. What is spooling? Do you think that advanced personal computers will have spooling as a standard feature in the future? 
		Раньше когда еще программы для компьютера загружали на тейпе, чтобы загрузить в комп программу, нужно было ждать завершения предыдущей. Spooling позволял загружать программу сразу же, компьютер сам загружал ее себе в освободившуюся часть. Опять же Танненбаум не дает четкого определения, но грубо говоря имеется в виду то, что компьютер не хочет хранить данные, поэтому передает их устройству, которому с этими данными надо работать. Самый яркий пример обычная печать - где есть очередь печати. Эта технология используется сейчас постоянно и в будущем тоже будет просто потому что у нее нет альтернатив.
6. On early computers, every byte of data read or written was handled by the CPU (i.e., there was no DMA). What implications does this have for multiprogramming? 
		Вызывалось аппаратное прерывание, которое требовало немедленной обработки процессором. После его передачи процессором в обработчик прерываний и завершения его работы возобновлялись все остальные процессы. С учетом DMA просто прерывание было короче, засчет того, что перенос данных совершался не процессором.
7. Whywas timesharing not widespread on second-generation computers? 
		Компьютеры 2 поколения это мэйнфреймы, которым давали на прочтение тейпы с программами на Фортране. Если даже код программы подается последовательно, то ни о каком разделении речи идти не может. Также сам компьютер просто не мог себе позволить обрабатывать прерывания, так как в то время любая система стоила очень дорого.
8. Instructions related to accessing I/O devices are typically privileged instructions, that is, they can be executed in kernel mode but not in user mode. Give a reason why these instructions are privileged. 
		Это непосредственная работа с аппаратным обеспечением, поэтому здесь нужен тотальный контроль. Какая-то мелкая ошибка может случайно отформатировать SSD. Именно поэтому пользовательским программам не дается доступ к этим инструкциям, а весь контроль над обработкой прерываний и данных берет на себя ОС.
9. One reason GUIs were initially slow to be adopted was the cost of the hardware need ed to support them. How much video RAM is needed to support a 25-line × 80-row character monochrome text screen? How much for a 1024 × 768-pixel 24-bit color bit map? What was the cost of this RAM at 1980 prices ($5/KB)? How much is it now?
       Кол-во памяти = кодировка * разрешение
       25 * 80 * 1байт( каждый символ кодируется 1 байтом) = 2000байт
       1024 * 768 * 24 = 18,874,368бит
       Стоимость =  (18,874,368 / 1024 / 8) * 5 = 11520$
10. There are several design goals in building an operating system, for example, resource utilization, timeliness, robustness, and so on. Give an example of two design goals that may contradict one another. 
		Я вообще не уверен, но вот 2 варианта: cкорость и безопасность, надежность и простота.
		Если программа работает быстро, значит какая-то ее часть упрощена, возможно часть, от которой зависит безопасность системы. Далее надежность и простота: приведу пример, для надежности, система разделяется на user mode и kernel mode и на так называемы rings. Да это ведет к улучшению безопасности, однако это же и ведет к усложнению самой архитектуры. PS: Я так подумал, что это по факту 1 и то же, но вообще я все правильно сказал
11. What is the difference between kernel and user mode? Explain how having two distinct modes aids in designing an operating system. 
		Обычные пользовательские программы не могут напрямую управлять аппаратным обеспечением, если бы могли, то любая скачанная программа могла бы буквально стереть вообще все данные или начать разгонять процессор. Такие программы  работают user mode. ОС же работает в kernel mode. Программы запущенные в kernel mode могут напрямую управлять аппаратным обеспечением. У них есть доступ  к kernel стеку каждого процесса.
12. A 255-GB disk has 65,536 cylinders with 255 sectors per track and 512 bytes per sec tor. How many platters and heads does this disk have? Assuming an average cylinder seek time of 11 msec, average rotational delay of 7 msec. and reading rate of 100 MB/sec, calculate the average time it will take to read 100 KB from one sector.
		У каждой пластины 2 рабочие поверхности. Если посчитать получается, что пластин 16, а головок 32. Общее время работы: 11 + 7 + 1 = 19мс.
13. Consider a system that has two CPUs, each CPU having two threads (hyperthreading). Suppose three programs, P0, P1, and P2, are started with run times of 5, 10 and 20 msec, respectively. How long will it take to complete the execution of these programs? Assume that all three programs are 100% CPU bound, do not block during execution, and do not change CPUs once assigned. 
		2 процессора, у каждого по 2 потока -> на 1 процессоре будут выполняться одновременно  P0 и P1 с замедление из-за hyperthreading. На 2 процессоре, будет выполняться процесс P2. Допустим замедление 0%. Тогда первые 2 потока выполняться за 10 секунд. Второй за 20 секунд. Тогда общее время 20 секунд.
14. List some differences between personal computer operating systems and mainframe operating systems.
		Операционный системы мэйнфреймов заточены на то, чтобы выполнять огромное количество несложных операций.  Вроде бы есть три типа: фоновые операции, быстрые операции и интерактивные сессии, когда пользователь активно взаимодейтсвует с машиной. ОС  ПК гораздо более многогранная и предназначена для других целей. В первую очередь она предназначена для работы 1 человека.
15. A computer has a pipeline with four stages. Each stage takes the same time to do its work, namely, 1 nsec. How many instructions per second can this machine execute? 
		1000000000 / 4 = 250000000инструкций. Стадия получения, стадия декодирования, стадия выполнения, стадия записи в регистр выполнения.
16. Consider a computer system that has cache memory, main memory (RAM) and disk, and an operating system that uses virtual memory. It takes 2 nsec to access a word from the cache, 10 nsec to access a word from the RAM, and 10 msec to access a word from the disk. If the cache hit rate is 95% and main memory hit rate (after a cache miss) is 99%, what is the average time to access a word?
		Вычислим по формуле матожидания
		M(X) = x1p1 + x2p2 + x3p3
		M(X) = 2 * 0.95 + 0.05 * 0.99 * 12 + 0.05 + 0.05 * 0.01 * 10000012
		M(X) = 5002.5 нс.
17. When a user program makes a system call to read or write a disk file, it provides an indication of which file it wants, a pointer to the data buffer, and the count. Control is then transferred to the operating system, which calls the appropriate driver. Suppose that the driver starts the disk and terminates until an interrupt occurs. In the case of reading from the disk, obviously the caller will have to be blocked (because there are no data for it). What about the case of writing to the disk? Need the caller be blocked awaiting completion of the disk transfer? 
		Процессу записи не нужно возвращать какие-то данные назад. Поэтому пока данные записываются на диск он может продолжать какие-то свои вычисление. Однако в таком случае намного сложнее обработать ошибку (дипсик выдал много разных способов, но я не думаю, что это очень важно сейчс), которая может произойти во время записи, например если пользователь выдернет флешку.
18. What is the key difference between a trap and an interrupt? 
		И trap и прерывание это сигналы, которые требуют немедленной обработки процессором.  Однако прерывание это внешний сигнал, исходящий из девайса, а trap это сигнал инициируемый программой. Есть еще одно отличие. Прерывание происходит асинхронно, а trap синхронно, зачастую, как результат какой-то команды.
19. Is there any reason why you might want to mount a file system on a nonempty direc tory? If so, what is it?
		Да, но я не сам до него догадался. Рассмотрим промышленный случай. Допустим у меня в основной памяти закончилось место. Я хочу монтировать жесткий диск к определенной папке. Но на этой папке есть файлы. Если бы это был ПК, можно было бы просто вырезать файлы, монтировать в пустой каталог диск, затем обратно вставить. Однако в промышленности так не получится. Пока файлы будут вырезаны, программа (например) сервера будет работать. Без этих файлов программа может сломаться или у нее просто не будет нужных данных. Тогда нужно сделать по другому. Я примонтирую просто куда-то диск, далее скопирую на него файлы и затем примонтирую в ту папку в которую мне надо. Есть несколько плюсов. Во-первых в конфигах программ не изменится путь. Во-вторых программа не будет останавливать свое действие 
20. What is the purpose of a system call in an operating system? 
		ОС должна предоставлять ПО в юзер моде абстракции для работы с железом. System call одна из таких абстракций. Программа просто вызывает его, когда хочет как-то взаимодействовать с железом, после чего вся работа передается ОС, и пользовательской программе интересно уже только то, что вернет систем колл.
21. Give one reason why mounting file systems is a better design option than prefixing path names with a drive name or number. Explain why file systems are almost always mounted on empty directories.
		Потому что если сделать так, чтобы девайсы могли становиться префиксами, возникает проблема.  При отсоединении девайса не очень ясно что делать с каталогами, префиксом которых был девайс. Они получаются просто висят и их нужно повторно монтировать. Но не очень понятно во-первых куда, а во вторых во всех программах которые на нее ссылаются придется менять путь. Файловые системы почти всегда монтируются в пустые директории  для того чтобы не скрывать файлы в каталоге.
22. For each of the following system calls, give a condition that causes it to fail: open, close, and lseek.
		open() - у пользователя нет прав, чтобы открыть файл.
		close() - не валидный файловый дескриптор
		lseek() - 3 аргумент вылезает за границы файлы( что кстати не всегда вызывает ошибку).
23. What type of multiplexing (time, space, or both) can be used for sharing the following resources: CPU, memory, SSD/disk, network card, printer, keyboard, and display? 
		Я сначала вообще вопрос не понял. Здесь рассматривается для каждого отдельного устройства. Процессор - время, поделить его никак нельзя. Память - пространство и время. Можно поделить на блоки памяти. Время - освобождение и заполнение. ССД тоже самое. Сетевая карта - только время, физически неделима. Принтер только время. Клавиатура только время. Дисплей - пространство.
24. Can the count = write(fd, buffer, nbytes); call return any value in count other than nbytes? If so, why? 
		Скорее всего, если запись была произведена неудачно, то вернется что-то вроде -1.
		PS: я так понял, что корректная запись происходит в несколько системных вызовов.
		То есть там есть цикл на запись. Это нужно потому, что write обращается по файловому дескриптору, но не знает к чему на самом деле обращается. Дипсик написал, про неблокируемые дескрипторы. Например сокеты(интерфейс для передачи данных между процессами). Их буфер может быть уже чем-то заполнен, поэтому программа записи будет итерировать пока не освободится место
25. A file whose file descriptor is fd contains the following sequence of bytes: 2, 7, 1, 8, 2, 8, 1, 8, 2, 8, 4. The following system calls are made: lseek(fd, 3, SEEK SET); read(fd, &buffer, 4); where the lseek call makes a seek to byte 3 of the file. What does buffer contain after the read has completed? 
		Так как параметр SEEK_SET, то указатель находится на 3 позиции от начала файла, то есть на 1. Тогда в буфер положатся байты  8 2 8 1. Индексация с нуля
26. Suppose that a 10-MB file is stored on a disk on the same track (track 50) in consecutive sectors. The disk arm is currently situated over track number 100. How long will it take to retrieve this file from the disk? Assume that it takes about 1 msec to move the arm from one cylinder to the next and about 5 msec for the sector where the beginning of the file is stored to rotate under the head. Also, assume that reading occurs at a rate of 100 MB/s. 
		Ему нужно будет со 100 перейти на 50, затем подождать пока начнется нужный сектор, затем прочитать.
		Получается 50 * 1msc + 5msc +100 msc = 155msc
27. What is the essential difference between a block special file and a character special file?
		Special file это одна из абстракций, которую ОС предоставляет для ПО.  По просто будет читать какое-то место в файле, а ОС будет делать все остальное. Block special файлы используются для устройств, чья память поддерживает произвольный доступ (random acsess), например жесткий диск, SSD, флеш-накопитель. Character special file используется для устройств, которые используют поток данных, например мышка.
28. In the example given in Fig. 1-17, the library procedure is called read and the system call itself is called read. Is it essential that both of these have the same name? If not, which one is more important
		Насколько я понимаю, имена system callov закреплены стандартом POSIX. Вообще желательно, чтобы у них было 1 и то же имя, что почти правда на UNIXlike системах.
		Однако например на Windows одна функция в библиотеке процедур, может содержать последовательное выполнение нескольких system коллов. Более важный системный вызов гораздо сложнее поменять, чем библиотечную процедуру.
29. ? 29. The client-server model is popular in distributed systems. Can it also be used in a sin gle-computer system?
		~~==Дистрибутивные системы - системы в которых несколько отдельных компьютеров работают отдельно друг от друга, но при этом вместе для пользователя являют собой 1 независимую систему. Мне кажется в таких системах клиенту необязательно знать, что именно происходит на сервере, ему просто нужно обработать его запрос. В singleOS пользователь является еще и администратором системы. У него должен быть доступ ко всему компьютеру. Также система запроса ответа просто не рациональна, когда всего 1 пользователь. Ведь он может имеет прямой доступ ко всей системе.==~~
		Вот правильный ответ: оно уже используется во множестве single систем. Сама концепция юзер мода и кернел мода это по сути и есть клиент-серверная модель.
30. To a programmer, a system call looks like any other call to a library procedure. Is it important that a programmer know which library procedures result in system calls? Under what circumstances and why? 
		Нет, потому что от него ничего не зависит. Вся работа по обработке системного вызова скидывается на ОС. Однако для определенного типа разработки это критически важно. Например - когда требуется высокая производительность, так как системный вызов очень дорогая операция. В системах реального времени, где требуется кристальная ясность происходящего.  Для кибербезопасника. 
31. Figure 1-23 shows that a number of UNIX system calls have no Win32 API equiv alents. For each of the calls listed as having no Win32 equivalent, what are the conse quences for a programmer of converting a UNIX program to run under Windows? 
		Это не просто замена вызовов, а глубокая архитектурная переработка. Программист должен не только выучить новые API, но и понять другую философию управления процессами, правами доступа и файловыми системами в Windows.
32. A portable operating system is one that can be ported from one system architecture to another without any modification. Explain why it is infeasible to build an operating system that is completely portable. Describe two high-level layers that you will have in designing an operating system that is highly portable.
		Невозможно написать портативную ОС по той причине, что есть фундаментальные различия между аппаратным обеспечением, которые требуют низкоуровневого кода. Яркий пример - процессор M1 не совместим с Windows. У Windows просто нет инструментов чтобы с ним работать. ~~Для высокой портативности, как мне кажется нужно очень много кода, в библиотеке процедур, который обернут в conditinal compilation. Тогда в зависимости от архитектуры, будет выполняться определенная часть кода.~~ 2 слоя: унификация самого нижнего слоя ядра, который отвечает за специфичные для аппаратного обеспечения детали. И унификация специфики конкретных устройств: уровень драйверов.
33. Explain how separation of policy and mechanism aids in building microkernel-based operating systems. 
		В таких системах микроядро выступает в роли слепого исполнителя. Оно 3просто делает, что ему говорят. Что ему делать, микроядру говорят сервера, которым в свою очередь это говорят пользовательские программы. Таким образом, микроядро является механизмом выполнения, а политикой приоретности занимаются сервера.
34. Virtual machines have become very popular for a variety of reasons. Nevertheless, they hav e some downsides. Name one.
		Во-первых - разделение ресурсов компьютера, на отдельные составляющие, замедляет общую мощность машины, потому что ресурсы тратятся еще и на распределение между виртуальными машинами, или binary transition инструкций.
		 Во-вторых, cкорее всего, из-за того, что нужно распределять ресурсы возникают уязвимости, с помощью которых могут нанести тяжелый урон по машине.
		
35. Here are some questions for practicing unit conversions: (a) How long is a microyear in seconds? (b) Micrometers are often called microns. How long is a gigamicron? (c) How many bytes are there in a 1-TB memory? (d) The mass of the earth is 6000 yottagrams. What is that in grams? 
		a) 60 * 60 * 24 * 365 / 1000000 = 31
		b)10 ** -6 * 10 ** 9 = 1000 метров.
		c)1 * 1024 * 1024 * 1024 * 1024 = 1099511627776
		d)6 * 10 ** 27 граммов
__________________________________________________________________________






36. Write a shell that is similar to Fig. 1-19 but contains enough code that it actually works so you can test it. You might also add some features such as redirection of input and output, pipes, and background jobs. 
			сделано
37. If you have a personal UNIX-like system (Linux, MINIX 3, FreeBSD, etc.) available that you can safely crash and reboot, write a shell script that attempts to create an unlimited number of child processes and observe what happens. Before running the experiment, type sync to the shell to flush the file system buffers to disk to avoid ruin ing the file system. You can also do the experiment safely in a virtual machine. Note: Do not try this on a shared system without first getting permission from the system administrator. The consequences will be instantly obvious so you are likely to be caught and sanctions may follow. 
			сделано
38. Examine and try to interpret the contents of a UNIX-like or Windows directory with a tool like the UNIX od program. (Hint: How you do this will depend upon what the OS allows. One trick that may work is to create a directory on a USB stick with one oper ating system and then read the raw device data using a different operating system that allows such access.idl
				