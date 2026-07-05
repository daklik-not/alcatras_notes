1. In Windows, when a user double clicks on a file listed by Windows Explorer, a pro gram is run and given that file as a parameter. List two different ways the operating system could know which program to run.
	Расширения файла, написанное в название.
	Сигнатуры файла.
2. In early UNIX systems, executable files (a.out files) began with a very specific magic number, not one chosen at random. These files began with a header, followed by the text and data segments. Why do you think a very specific number was chosen for executable files, whereas other file types had a more-or-less random magic number as the first word?
		Потому что для ОС особенно важно отделять исполняемые файлы от неисполняемых - исполняемый файл интерпретируется ядром, как структура.
3. In Fig. 4-5, one of the attributes is the record length. Why does the operating system ev er care about this?
	The record-length, key-position, and key-length fields are only present in files whose records can be looked up using a key - цитата из учебника. Можно сделать вывод, что это key-indexed файлы. Размер записи должен быть фиксированным, для того, чтобы при обращении к файлу ФС могло корректно искать номер записи/блока, иначе тяжело понять где начинается следующий ключ-запись/блок.
4. Is the open system call in UNIX absolutely essential? What would the consequences be of not having it?
	При вызове open() ОС читает файл директории, в которой находится файл, оттуда получает инод.  Потом по иноду в своих внутренних структурах определяет местоположение файлов и находит, в зависимости от ФС, структуру, с помощью которой зная один блок мы можем найти остальные. При последующих вызовах read() мы обращаемся сначала по индексу к структуре ядра по индексу fd, и оттуда уже на инод.  Если бы не было open(), ФС каждый раз приходилось бы проходить pathname с рабочей/корневой директории. Это гарантированные лишние обращения к диску - замедление работы.
5. Systems that support sequential files always have an operation to rewind files. Do sys tems that support random-access files need this, too?
	   Мне кажется что нет. На современных ОС иноды напрямую хранят адрес блоков файла. Если мы хотим еще раз прочитать, то просто обратимся еще раз - перечитать блок достаточно быстро, так как он маленький.
6. Some operating systems provide a system call rename to give a file a new name. Is there any difference at all between using this call to rename a file and just copying the file to a new file with the new name, followed by deleting the old one?
		Обновление структур ядра быстрее, чем перекопировать полностью файл и записывать его, особенно если файл большой. Так что это приведет к падению скорости.+rename, как пишет chatGPT, rename атомарен, это уменьшает вероятность нестабильного состояния.
7. A simple operating system supports only a single directory but allows it to have arbi trarily many files with arbitrarily long file names. Can something approximating a hier archical file system be simulated? How?
		Можно попробовать создать файл, который будет содержать имена файлов, и обращаться только через него. Или поддерживать специальный формат для имен файла вроде dir1/file. Но насколько я понимаю в это не очень много смысла если все равно можно просто обратиться по имени.
8. In UNIX and Windows, random access is done by having a special system call that moves the ‘‘current position’’ pointer associated with a file to a given byte in the file. Propose an alternative way to do random access without having this system call.
		Вместо того чтобы сначала двигать seek, и потом читать, будем передавать сразу байт с которого надо читать в read(fd, offset, buffer, nbytes).
9. Consider the directory tree of Fig. 4-9. If /usr/jim is the working directory, what is the absolute path name for the file whose relative path name is ../ast/x?
		/usr/ast/x
10. Contiguous allocation of files leads to disk fragmentation, as mentioned in the text, because some space in the last disk block will be wasted in files whose length is not an integral number of blocks. Is this internal fragmentation or external fragmentation? Make an analogy with something discussed in the previous chapter.
		внутренняя фрагментация. аналогия - в paging так же последняя страница заполнялась не полностью.
11. Suppose a filesystem check reveals that a block has been allocated to two different files, /home/hjb/dadjokes.txt and /etc/motd. Both are text files. The filesystem check duplicates the block’s data and re-assigns /etc/motd to use the new block. Answer the following questions. (i) In what realistic circumstance(s) could the data from both files still remain correct and consistent with their original content? (ii) How might the user investigate whether the files have been corrupted? (iii) If one or both of the files’ data have been corrupted, what mechanisms might allow the user to recover the data?
	1) если файл выделил блок, но ничего не записал туда. 
	2) Посмотрим иноды файлов чтобы посчитать сколько раз используется каждый блок, если блок используется больше 1 раза - FS inconsistency, это делает ОС.  Пользователь просто может посмотреть разницу с последней актуальной версией файла, на наличие изменений, которые не должны были произойти
	3) Журналируемые ФС, бэкапы.
	
12. One way to use contiguous allocation of the disk and not suffer from holes is to com pact the disk every time a file is removed. Since all files are contiguous, copying a file requires a seek and rotational delay to read the file, followed by the transfer at full speed. Writing the file back requires the same work. Assuming a seek time of 5 msec, a rotational delay of 4 msec, a transfer rate of 8 MB/sec, and an average file size of 8 KB, how long does it take to read a file into main memory and then write it back to the disk at a new location? Using these numbers, how long would it take to compact half of a 16-GB disk?
		8 / (8 \* 1024 ) \* 1000 ~ 1ms - время чистой записи файла
		 5 + 4 + 1 = 10ms полное время записи файла
		 10ms \* 2 = 20ms чтение и запись.
		 8\* 1024 \* 1024 /  8  = 1,048,576 файлов на диске.
		 Время компактизации -  1,048,576 \* 20 =20,971,520ms;
	Ну короче очень медленно.
	
13. MacOS has symbolic links and also aliases. An alias is similar to a symbolic link; however, unlike symbolic links, an alias stores additional metadata about the target file (such as its inode number and file size) so that, if the target file is moved within the same filesystem, accessing the alias will result in accessing the target file, as the filesystem will search for and find the original target. How could this behavior be ben eficial compared to symbolic links? How could it cause problems?
		В симлинке, когда мы переносим файл, мы должны вручную обновить или пересоздать LINK файл. Здесь мы ищем файл по описанию. Такой подход очень медленный - если файл перенесен в рандомное место в ФС, то понадобится немалое время чтобы найти его по описанию. Также нужно обновлять структуры самого альяса при повторном открытии файла, например - путь, номер инода и так далее.
14. Following on the previous question, in earlier MacOS versions, if the target file is moved and then another file is created with the original path of the target, the alias would still find and use the moved target file (not the new file with the same path/name). However, in versions of MacOS 10.2 or later, if the target file is moved and another is created in the old location, the alias will connect to the new file. Does this address the drawbacks from your answer to the previous question? Does it dampen the benefits you noted?
		1)Нет, macos делает это намеренно
		1)Да, теперь мы не гарантированно находим файл, зная альяс
	
15. Some digital consumer devices need to store data, for example as files. Name a modern device that requires file storage and for which contiguous allocation would be a fine idea.
		Например цифровые фотоаппараты - все фотографии одинакового размера, следовательно внешней фрагментации не возникает. Вообще подойдет любое устройство чьи файлы относительно одинаковые в размерах
16. Consider the i-node shown in Fig. 4-15. If it contains 10 direct addresses of 4 bytes each and all disk blocks are 1024 KB, what is the largest possible file?
		На рисунке 7 прямых адресов на блоки и один адрес на блок указателей. Я так полагаю имеется в виду, что если бы было 10 адресов и 1 блок указателей. Тогда 10 адресов блоков напрямую + 1024  * \ 1024 / 4 = 262,144 + 262154 блоков можно адресовать - 256ГБ файл.
17. For a given class, the student records are stored in a file. The records are randomly accessed and updated. Assume that each student’s record is of fixed size. Which of the three allocation schemes (contiguous, linked and table/indexed) will be most appropri ate?
		Единственный минус contigious аллокация - внешняя фрагментация. Если все записи фиксированного размера, то это устраняет его. +у непрерывной аллокации намного проще реализация и администрирование чем у других подходов.
18. Consider a file whose size varies between 4 KB and 4 MB during its lifetime. Which of the three allocation schemes (contiguous, linked and table/indexed) will be most appropriate?
		Вообще в таком случае табличная или индексированная. Линкед лист почти всегда плох из-за того, что доступ делается последовательно через все блоки.
19. It has been suggested that efficiency could be improved and disk space saved by stor ing the data of a short file within the i-node. For the i-node of Fig. 4-15, how many bytes of data could be stored inside the i-node?
		4 \* 8 = 32 байта, поскольку если хранить байты на блоке с адресами, то фактически это тоже самое, что и просто хранить на диске.
20. Tw o computer science students, Carolyn and Elinor, are having a discussion about i nodes. Carolyn maintains that memories have gotten so large and so cheap that when a file is opened, it is simpler and faster just to fetch a new copy of the i-node into the i node table, rather than search the entire table to see if it is already there. Elinor dis agrees. Who is right?
		Так или иначе, когда память забьется, а если не очищать иноды она забьется, то нам надо будет их удалять. Тогда встает вопрос а что удалять - нам все равно придется искать эти иноды в таблице. Поэтому вместо копии лучше все таки искать старую - поэтому Элинор права как по мне.
21. Name one advantage of hard links over symbolic links and one advantage of symbolic links over hard links.
		Хард линки быстрее, потому что не надо проходит по полному пути в LINK файле. Символические ссылки лучше тем, что когда владелец удаляет файл, то все симлинки автоматически становятся нерабочими. В это же время хардлинки продолжают ссылаться на несуществующий файл.
22. Explain how hard links and soft links differ with respective to i-node allocations.
		У хард-линкованных файлов 1 инод. Для симлинков создается новый инод файла LINK
23. Consider a 4-TB disk that uses 8-KB blocks and the free-list method. How many block addresses can be stored in one block?
	    log2(4 \* 1024 \* 1024 \* 1024 /  8) - 29битное число нужно - 4байта
	    8 \* 1024  / 4 = 2048 адресов в 1 блоке.
24. Free disk space can be kept track of using a free list or a bitmap. Disk addresses require D bits. For a disk with B blocks, F of which are free, state the condition under which the free list uses less space than the bitmap. For D having the value 16 bits, express your answer as a percentage of the disk space that must be free.
		Количество места занятое битовой картой - по одному биту на блок то есть B бит
		Количество места занятого ССБ - D \* F бит
		D \* F  < B - условие
		Для D  =16 ответ 6.25% должно быть свободно меньше этого числа

25. The beginning of a free-space bitmap looks like this after the disk partition is first for matted: 1000 0000 0000 0000 (the first block is used by the root directory). The sys tem always searches for free blocks starting at the lowest-numbered block, so after writing file A, which uses six blocks, the bitmap looks like this: 1111 1110 0000 0000. Show the bitmap after each of the following additional actions: 
		(a) File B is written, using fiv e blocks.  -  1111 1111 1111 0000.
		 (b) File A is deleted. - -  1000 0001 1111 0000.
		 (c) File C is written, using eight blocks. - 1111 1111 1111 1100.
		 (d) File B is deleted. -1111 1110 0000 1100.
	
26. What would happen if the bitmap or free list containing the information about free disk blocks was completely lost due to a crash? Is there any way to recover from this disas ter, or is it bye-bye disk? Discuss your answers for UNIX and the FAT -16 file system separately.
		В fat системах достаточно просто пробежаться по всей FAT таблице и дополнением к множеству блоков, которые есть в этой таблице будут свободные блоки
		В unix нужно пробежаться по все файлам директорий, для каждого инода посмотреть занятые блоки, и составить глобальную страницу -  дополнением к множеству блоков, которые есть в этой таблице будут свободные блоки
27. Oliver Owl’s night job at the university computing center is to change the tapes used for overnight data backups. While waiting for each tape to complete, he works on writ ing his thesis that proves Shakespeare’s plays were written by extraterrestrial visitors. His text processor runs on the system being backed up since that is the only one they have. Is there a problem with this arrangement?
		Любой неатомарный бэкап приводит к не консистентному состоянию. Тем не менее если бэкапы делаются снимками+CoW, то все норм должно быть
28. We discussed making incremental dumps in some detail in the text. In Windows it is easy to tell when to dump a file because every file has an archive bit. This bit is miss ing in UNIX. How do UNIX backup programs know which files to dump?
		Like the i-node of Fig. 4-15, the UNIX i-node contains some attributes. The attributes contain the file size, three times (creation, last access, and last modifica tion), - цитата из книги. Тогда программы будут понимать по биту последней модификации
29. Suppose that file 21 in Fig. 4-27 was not modified since the last dump. In what way would the four bitmaps of Fig. 4-28 be different?
		Мне лень все пересматривать но основная идея в том, что файл бы не дампился, и если в директории, в которой находится файл, только он был модифицированным, то и директория то же не будет дампится. Аналогично с директориями выше в дереве.
30. It has been suggested that the first part of each UNIX file be kept in the same disk block as its i-node. What good would this do?
		Насколько я понял главная причина в том, что иногда бывает полезно за одно обращение получить начальные данные файла - формат, размер. Также иногда бывают очень маленькие файлы - тогда мы за одно обращение читаем и инод и файл.
31. Consider Fig. 4-29. Is it possible that for some particular block number the counters in both lists have the value 2? How should this problem be corrected?
		Создается файл, блок добавляется в инод, но при этом ОС крашит и не убирает его из ССБ. Создается второй файл он видит свободный блок первого, забирает его себе. Оба файла открыты и ссылаются на один и тот же блок.
		Первый файл закрывается ОС крашит и файл не убирается из ССБ, также для второго файла
		Я не знаю насколько вообще реалистична такая ситуация, но для ее решения ОС должна определить какому файлу отойдет блок, для другого выделит новый и поменять его инод.
32. The performance of a file system depends upon the cache hit rate (fraction of blocks found in the cache). If it takes 1 msec to satisfy a request from the cache, but 40 msec to satisfy a request if a disk read is needed, give a formula for the mean time required to satisfy a request if the hit rate is h. Plot this function for values of h varying from 0 to 1.0.
```c
from matplotlib import pyplot as plt
a = []
for i in range(1,100):
    h = i / 100
    mean = 40 * (1 - h) + h * 1
    a.append(mean)
plt.plot(a)
plt.show()
```
![[Pasted image 20260203021131.png]]
33. For an external USB hard drive attached to a computer, which is more suitable: a write through cache or a block cache?
		write through cache - поскольку неизвестно, когда юзер вытянет флешку, при этом он может не использовать безопасно извлечение, тогда все модифицированные данные потеряются
34. Consider an application where students’ records are stored in a file. The application takes a student ID as input and subsequently reads, updates, and writes the correspond ing student record; this is repeated till the application quits. Would the ‘‘block read ahead’’ technique be useful here?
		Нет, потому что не гарантируется что id студентов будут последовательными - следующий студент выбирается рандомно - мы просто не знаем, откуда читать.
35. Discuss the design issues involved in selecting the appropriate block size for a file system.
		При большом размере блока увеличивается внутренняя фрагментация для маленьких файлов. При маленьком размере файл становится раздробленным - сильно замедляется его чтение + увеличивается размер таблицы в RAM, а это ценный ресурс. 
36. Consider a disk that has 10 data blocks starting from block 14 through 23. Let there be 2 files on the disk: f1 and f2. The directory structure lists that the first data blocks of f1 and f2 are, respectively, 22 and 16. Given the FAT table entries as below, what are the data blocks allotted to f1 and f2?
 ```
(14,18); (15,17); (16,23); (17,21); (18,20); (19,15); (20, 1); (21, 1); (22,19); (23,14). 
 ```
 In the above notation, (x, y) indicates that the value stored in table entry x points to data block y.
		22 - 19 - 15 -17 - 21;
		16 - 23 -14 -18 - 20 - 1

37. In the text, we discussed two major ways to identify file type: file extensions and inves tigation of file content (e.g., by using headers and magic numbers). Many modern UNIX filesystems support extended attributes which can store additional metadata for a file, including file type. This data is stored as part of the file’s attribute data (in the same way that file size and permissions are stored). How is the extended attribute approach for storing files better or worse than the file extension approach or identi fying file type by content?
		Подход с расширенными атрибутами лучше тем, что ОС независимо от изменяемого имени может понять тип файла
		Подход с расширениями лучше тем, что он более user-friendly - пользователь сразу видит с каким файлом имеет дело.
38. Consider the idea behind Fig. 4-23, but now for a disk with a mean seek time of 8 msec, a rotational rate of 15,000 rpm, and 262,144 bytes per track. What are the data rates for block sizes of 1 KB, 2 KB, and 4 KB, respectively?
		За сколько делается 1 оборот милисекунд $60 / 15000 = 4ms$
		Скорость чтения - $262144  / 4 = 65,536 b/ms = 64KB/ms$
		Время чтения 1KB - $8 + 0.015$
		Время чтения 2KB - $8 + 0.031$
		Время чтения 4KB - $8 + 0.0625$
		Скорее всего на примере этого задания автор хочет показать, что самая операция чтения очень быстрая - медленный seek time.
39. In this chapter, we hav e seen that SSDs do their best to avoid writing the same memory cells frequently (because of the wear). However, many SSDs offer much more func tionality than what we presented so far. For instance, many controllers implement compression. Explain why compression may help with reducing the wear.
		Чем меньше ячеек занимаем - тем меньше ячеек изнашивается. Сжатие дает уменьшение размера файла - уменьшение количества используемых ячеек.
40. Given a disk-block size of 4 KB and block-pointer address value of 4 bytes, what is the largest file size (in bytes) that can be accessed using 11 direct addresses and one indi rect block?
		11 блоков через директ адреса можно адресовать.
		4 \* 1024 / 4 = 1024 адреса можно сохранить в индирект блоке.
		(1024 +11) \* 4 = 4,140KB
41. The MS-DOS FAT -16 table contains 64K entries. Suppose that one of the bits had been needed for some other purpose and that the table contained exactly 32,768 entries instead. With no other changes, what would the largest MS-DOS file have been under this condition?
		32768 \* 512байт - 16МБ
42. Files in MS-DOS have to compete for space in the FAT -16 table in memory. If one file uses k entries, that is k entries that are not available to any other file, what constraint does this place on the total length of all files combined?
		Суммарное число записей кластеров файлов не должно превышать доступное количество записей в таблице.
43. How many disk operations are needed to fetch the i-node for a file with the path name /usr/ast/courses/os/handout.t? Assume that the i-node for the root directory is in mem ory, but nothing else along the path is in memory. Also assume that all directories fit in one disk block.
		Для каждой директории/файла нужно сфетчить ее инод, потом ее файл.
		Тогда 1 + 2 + 2 + 2 + 2 + 1 = 10
44. In many UNIX systems, the i-nodes are kept at the start of the disk. An alternative design is to allocate an i-node when a file is created and put the i-node at the start of the first block of the file. Discuss the pros and cons of this alternative.ъ
		Плюс такого подхода в том, что это намного эффективнее для маленьких файлов < размера блока - только 1 чтение с диска.
		Минус в замедлении скорости поиска инода. В классических системах иноды хранятся в непрерывной структуре, к которой можно обратиться по индексу. Теперь каждый инод нужно будет отдельно искать по блокам в ФС.
45. Write a program that reverses the bytes of a file, so that the last byte is now first and the first byte is now last. It must work with an arbitrarily long file, but try to make it reasonably efficient.
    Основная моя ошибка, что read() надо делать в цикле как в примере. Но цикл несложно добавить но долго, поэтому я так оставлю - upt - переделал
	```c


#include <sys/types.h>
#include <fcntl.h>
#include <stdlib.h>
#include <iostream>
#include <unistd.h>
#include <sys/stat.h> //библиотека для получения информации о файле

const int BLOCK_SIZE = 4096;
void reverse(char buf[], int size) {
    for (size_t i = 0; i < size / 2; ++i) {
        char temp = buf[i];
        buf[i] = buf[size - 1 - i];  // -1 здесь!
        buf[size - 1 - i] = temp;
    }
}

void out(char buf[]) {
    for (int i = 0 ; i < BLOCK_SIZE; ++i) printf("%c", buf[i]);
    printf("\n");
}
int main() {
    struct stat st;
    int fd, rd_count, wt_count;
    char fblock[BLOCK_SIZE], sblock[BLOCK_SIZE];
    char *lastBlock;
    fd = open("firstsequence.txt", O_RDWR);
    if (fd < 0) exit(1);
    int counter = 0;
    fstat(fd, &st); // получили всю информацию о структурах
    while (true) {
        int first_node = BLOCK_SIZE * counter;
        int second_node = st.st_size - BLOCK_SIZE * (counter + 1);
        int dist = second_node - first_node;
        if (dist < BLOCK_SIZE) {
            lseek(fd, first_node, SEEK_SET);
            //прочитать одну вершину
            if (first_node == second_node) {
                  //  printf("here1");
                int readen =1e9;
                while (readen > 0) readen =  read(fd, fblock, BLOCK_SIZE);
                lseek(fd, first_node, SEEK_SET);
                reverse(fblock, BLOCK_SIZE);
                write(fd, fblock, BLOCK_SIZE);
            }

            else if (dist < 0) { //dist был < 8 но больше 4 случай не равен 4,это когда просто обмен
                 //printf("here2");
                int readen =1e9;
                while (readen > 0) readen = read(fd, fblock, second_node + BLOCK_SIZE - first_node);
                lseek(fd, first_node, SEEK_SET);
                reverse(fblock, second_node + BLOCK_SIZE - first_node);
                write(fd, fblock, second_node + BLOCK_SIZE - first_node);
            } else if (dist > 0) {
                //printf("here3");
                int readen =1e9;
                while (readen > 0) readen = read(fd, fblock, second_node - first_node);
                readen = 1e9;
                while (readen > 0) readen = read(fd, sblock, BLOCK_SIZE);
                lseek(fd, first_node, SEEK_SET);
                reverse(fblock, second_node - first_node);
                reverse(sblock, BLOCK_SIZE);
                write(fd, sblock, BLOCK_SIZE);
                write(fd, fblock, second_node - first_node);
            }
            break;
        }

        lseek(fd, first_node, SEEK_SET);
        int readen = 1e9;
        while (readen > 0) readen = read(fd, fblock, BLOCK_SIZE);
        //прочитали начало
        readen = 1e9;
        lseek(fd, second_node, SEEK_SET); //передвинули на последние
        while (readen > 0) readen = read(fd, sblock, BLOCK_SIZE);

        reverse(fblock, BLOCK_SIZE);
        reverse(sblock, BLOCK_SIZE);


        lseek(fd, first_node, SEEK_SET);
        write(fd, sblock, BLOCK_SIZE);
        lseek(fd, second_node, SEEK_SET);
        write(fd, fblock, BLOCK_SIZE);
        counter++;
    }
}
	```
46. Write a program that starts at a given directory and descends the file tree from that point recording the sizes of all the files it finds. When it is all done, it should print a histogram of the file sizes using a bin width specified as a parameter (e.g., with 1024, file sizes of 0 to 1023 go in one bin, 1024 to 2047 go in the next bin, etc.).
	Гистограмма - из-за того что раброс файлов очень большой диаграмму просто не строит с теми размерами блоков
```C
	#include <iostream>
#include <dirent.h>
#include <cstdlib>
#include <cstring>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
long long file_sizes = 0;
int fd;
void check_directory(char* path) {
    DIR *dir;
    dir = opendir(path);
    if (!dir) {
        std::cerr << "cant open";
        return;
    }
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        bool expression = (strcmp(entry->d_name, ".") && strcmp(entry->d_name, ".."));
        if (!expression) continue; // обработка . и ..
        char* p_path = new char[strlen(path) + 2 + strlen(entry->d_name)];
        strcpy(p_path, path); //скопировали в начало p_path
        strcat(p_path, "/");
        strcat(p_path, entry->d_name);//c-style конкантенация строк.
        if ((entry->d_type == DT_DIR)) {//directory
             //for \n + 1
            check_directory(p_path);
        }
        struct stat buf;
        stat(p_path, &buf);
        char buffer[20];
        if (buf.st_size != 0) {
            snprintf(buffer, sizeof(buffer),"%lld\n", buf.st_size);
            write(fd, buffer, strlen(buffer));
            file_sizes += buf.st_size;
        }

        delete[] p_path;
    }
    closedir(dir);
    return;
}

int main()
{
    fd = open("firstsequence.txt", O_RDWR);

    check_directory("E:/");
    return 0;
}

```
 ![[Pasted image 20260205134227.png]]
 
 48. Write a new version of the UNIX ls program. This version takes as an argument one or more directory names and for each directory lists all the files in that directory, one line per file. Each field should be formatted in a reasonable way given its type. List only the first disk address, if any.
 ```c
 #include <iostream>
#include <dirent.h>
#include <cstdlib>
#include <cstring>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <pwd.h>
#include <grp.h>

void make_rights(char (&rights)[], struct stat inode) {
    if (inode.st_mode & S_IRUSR) rights[1] = 'r';
        if (inode.st_mode & S_IWUSR) rights[2] = 'w';
        if (inode.st_mode & S_IXUSR) rights[3] = 'x';

        if (inode.st_mode & S_IRGRP) rights[4] = 'r';
        if (inode.st_mode & S_IWGRP) rights[5] = 'w';
        if (inode.st_mode & S_IXGRP) rights[6] = 'x';

        if (inode.st_mode & S_IROTH) rights[7] = 'r';
        if (inode.st_mode & S_IWOTH) rights[8] = 'w';
        if (inode.st_mode & S_IXOTH) rights[9] = 'x';
}

char get_file_type_char(mode_t mode) { //это дипсиком, потому это скучно просто  делать
    switch (mode & S_IFMT) {
        case S_IFREG:  return '-';
        case S_IFDIR:  return 'd';
        case S_IFCHR:  return 'c';
        case S_IFBLK:  return 'b';
        case S_IFIFO:  return 'p';
        case S_IFLNK:  return 'l';
        case S_IFSOCK: return 's';
        default:       return '?';
    }
}

void print_time(time_t t) {
    struct tm *tm_info = localtime(&t);
    char timebuf[80];
    time_t now = time(NULL);

    // Если файл модифицирован в текущем году И разница меньше 6 месяцев
    if (difftime(now, t) < 15778463) {  // ~6 месяцев в секундах
        strftime(timebuf, sizeof(timebuf), "%b %d %H:%M", tm_info);
    } else {
        strftime(timebuf, sizeof(timebuf), "%b %d  %Y", tm_info);
    }

    printf("%s\n", timebuf);
}

void list_files(char *path) {
    chdir(path);

    DIR *dir;
    struct dirent *entry;
    dir = opendir(".");
    while ((entry = readdir(dir)) != NULL) {
        struct stat inode;
        stat(entry->d_name, &inode);  // ОШИБКА: stat для "." после chdir

        char rights[11] = "---------";  // 10 символов + '\0' = 11, правильно
        rights[0] = get_file_type_char(inode.st_mode);  // тип в начало
        make_rights(rights, inode);
        struct passwd *pwd = getpwuid(inode.st_uid);
        struct group *grp = getgrgid(inode.st_gid);
        printf("%s %lu %s %s %lld %s %lu ",
               rights,
               (unsigned long)inode.st_nlink,
               pwd->pw_name, grp->gr_name,
               inode.st_size,
               entry->d_name,
               inode.st_ino
        );
        print_time(inode.st_mtime);
    }
    closedir(dir);
}

void ls(int argc, char *argv[]) {
    if (argc < 2) {
        perror("too few arguments");
    }
    for (int i = 0 ; i < argc - 1; ++i) { //ls path1 path2
        list_files(argv[i]);
    }
}

int main()
{
    char* a[] = {"C:/Users/0987a/OneDrive/Рабочий стол/iris/message passing/"};
    ls(2, a);
}

 ```
49. Implement a program to measure the impact of application-level buffer sizes on read time. This involves writing to and reading from a large file (say, 2 GB). Vary the appli cation buffer size (say, from 64 bytes to 4 KB). Use timing measurement routines (such as gettimeofday and getitimer on UNIX) to measure the time taken for different buffer sizes. Analyze the results and report your findings: does buffer size make a difference to the overall write time and per-write time?
```c
#include <iostream>
#include <dirent.h>
#include <cstdlib>
#include <cstring>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <chrono>
#include <string>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <pwd.h>
#include <grp.h>
#define ll long long
const ll BUF_SIZE = 4096;
const ll TOTAL_BYTES = 2147483648LL;
int main()
{
    auto start = std::chrono::high_resolution_clock::now();
    ll rd_count, wt_count;
    ll fd = open("firstsequence.txt", O_RDWR);
    if (fd < 0) perror("cant open file");
    char buf[BUF_SIZE];  // BUF_SIZE в байтах!
    for (ll i = 0 ; i < BUF_SIZE; ++i) buf[i] = 'a';
    for (ll i = 0; i < TOTAL_BYTES; i += BUF_SIZE) {
        ll bytes_to_write = std::min(BUF_SIZE, TOTAL_BYTES - i);
        write(fd, buf, bytes_to_write);
    }
    lseek(fd, 0, SEEK_SET);
    while (true) {
        rd_count = read(fd, buf, BUF_SIZE);
        if (rd_count <= 0) break;
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = end - start;
    std::cout << duration << std::endl;
}
```

| Буфер | Время          |
| ----- | -------------- |
| 64    | 152710726600ns |
| 128   | 77163105900ns  |
| 256   | 40368798100ns  |
| 512   | 20576959200ns  |
| 1024  | 14846091100ns  |
| 2048  | 11593271300ns  |
| 4096  | 10721732500ns  |
50. Implement a simulated file system that will be fully contained in a single regular file stored on the disk. This disk file will contain directories, i-nodes, free-block infor mation, file data blocks, etc. Choose appropriate algorithms for maintaining free-block information and for allocating data blocks (contiguous, indexed, linked). Your program will accept system commands from the user to perform file system operations, includ ing at least one to create/delete directories, create/delete/open files, read/write from/to a selected file, and to list directory contents.э
Это крупный проект на несколько недель) У меня пока что просто нет времени на него но может быть я когда нибудь вернусь к нему