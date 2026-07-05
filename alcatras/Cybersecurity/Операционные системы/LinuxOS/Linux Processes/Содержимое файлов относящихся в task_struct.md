Файл /proc/PID/status
```
Name:   test //имя процесса
Umask:  0022 //маска прав на создаваемый файлы
State:  R (running) // состояние

Tgid:   914  |
Ngid:   0    | 
			 | идентефикаторы
Pid:    914  |
PPid:   775  |

TracerPid:      0
Uid:    1000    1000    1000    1000
Gid:    1000    1000    1000    1000
FDSize: 256
Groups: 4 24 27 30 46 100 1000
NStgid: 914
NSpid:  914
NSpgid: 914
NSsid:  775
Kthread:        0 // не является потоком ядра
VmPeak:     2584 kB // пиковый размер виртуальной памяти
VmSize:     2548 kB // текущий размер
VmLck:         0 kB
VmPin:         0 kB
VmHWM:      1024 kB
VmRSS:      1024 kB // физическая память, используемая процессом.
RssAnon:               0 kB
RssFile:   1024 kB // физическая память используемая отображенными файлами
RssShmem:              0 kB
VmData:       92 kB //размер сегмента данных
VmStk:       132 kB //размер сегмента стека
VmExe:         4 kB //размер кода
VmLib:      1748 kB //размер разделяемых библиотек
VmPTE:        40 kB
VmSwap:        0 kB //память вытесненная в swap
HugetlbPages:          0 kB
CoreDumping:    0
THP_enabled:    1
untag_mask:     0xffffffffffffffff
Threads:        1 // количество потоков в процессе
SigQ:   1/31619

SigPnd: 0000000000000000 // какие в процессе доставки
ShdPnd: 0000000000000000
SigBlk: 0000000000000000 // какие заблокированы
SigIgn: 0000000000000000 // какие игнорируются
SigCgt: 0000000000000000 // какие перехватываются
CapInh: 0000000000000000 
CapPrm: 0000000000000000
CapEff: 0000000000000000
CapBnd: 000001ffffffffff
CapAmb: 0000000000000000
NoNewPrivs:     0
Seccomp:        0
Seccomp_filters:        0
Speculation_Store_Bypass:       thread vulnerable
SpeculationIndirectBranch:      conditional enabled
Cpus_allowed:   3f
Cpus_allowed_list:      0-5
Mems_allowed:   00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000000,00000001
Mems_allowed_list:      0
voluntary_ctxt_switches:        1
nonvoluntary_ctxt_switches:     502
```

#### Директория /proc/PID/fd/
Символические ссылки на все открытые процессом файлы
```
lrwx------ 1 daklik_not daklik_not 64 May 11 19:23 0 -> /dev/pts/2
lrwx------ 1 daklik_not daklik_not 64 May 11 19:23 1 -> /dev/pts/2
lrwx------ 1 daklik_not daklik_not 64 May 11 19:23 2 -> /dev/pts/2
lrwx------ 1 daklik_not daklik_not 64 May 11 19:23 3 -> /home/daklik_not/learning/file.txt // реально открый программой файл
```

#### Файл /proc/PID/fdinfo/[fd]
```c
pos:    0 - lseek
flags:  0100002 - флаги с которыми был открыт
mnt_id: 80 - можно узнать на каком устройстве и в какой директори смонтирована ФС содержащая данныый файл
ino:    6715 - номер инода
```

#### Файл /proc/PID/sched
Содержит информацию нужную для планирования процесса. Несложно догадаться что файл постоянно меняется. Есть еще файл **stat**
```c
test (985, #threads: 1)
-------------------------------------------------------------------
se.exec_start                                :      18693697.869300
se.vruntime                                  :       2146638.134424
se.sum_exec_runtime                          :      16524055.967800
se.nr_migrations                             :                    3
nr_switches                                  :                54433
nr_voluntary_switches                        :                    1
nr_involuntary_switches                      :                54432
se.load.weight                               :              1048576
se.avg.load_sum                              :                47262
se.avg.runnable_sum                          :             48402459
se.avg.util_sum                              :             48400648
se.avg.load_avg                              :                 1023
se.avg.runnable_avg                          :                 1024
se.avg.util_avg                              :                 1023
se.avg.last_update_time                      :       18693697868800
se.avg.util_est.ewma                         :                  512
se.avg.util_est.enqueued                     :                  512
policy                                       :                    0
prio                                         :                  120
se.slice                                     :              2250000
clock-delta                                  :                    0
```

#### Файл /proc/PID/maps
Ну вообще там много файлов, которые относятся к memory-management, но этот вроде прям наглядно все показывает.  В коде только маленький отрывок файла. Есть еще файл pagemap но его невозможно прочитать.
```

b60720000-634b60721000 r--p 00000000 08:30 73135                      /home/daklik_not/learning/test
634b60721000-634b60722000 r-xp 00001000 08:30 73135                      /home/daklik_not/learning/test
634b60722000-634b60723000 r--p 00002000 08:30 73135                      /home/daklik_not/learning/test
634b60723000-634b60724000 r--p 00002000 08:30 73135                      /home/daklik_not/learning/test
634b60724000-634b60725000 rw-p 00003000 08:30 73135                      /home/daklik_not/learning/test
634b6d13d000-634b6d15e000 rw-p 00000000 00:00 0                          [heap]
774e73e00000-774e73e28000 r--p 00000000 08:30 38603                      /usr/lib/x86_64-linux-gnu/libc.so.6
774e73e28000-774e73fb0000 r-xp 00028000 08:30 38603                      /usr/lib/x86_64-linux-gnu/libc.so.6
774e73fb0000-774e73fff000 r--p 001b0000 08:30 38603                      /usr/lib/x86_64-linux-gnu/libc.so.6
774e73fff000-774e74003000 r--p 001fe000 08:30 38603                      /usr/lib/x86_64-linux-gnu/libc.so.6
774e74003000-774e74005000 rw-p 00202000 08:30 38603                      /usr/lib/x86_64-linux-gnu/libc.so.6
774e74005000-774e74012000 rw-p 00000000 00:00 0
774e741d2000-774e741d6000 r--p 00000000 08:30 43849                      /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
774e741d6000-774e741fa000 r-xp 00004000 08:30 43849                      /usr/lib/x86_64-linux-gnu/lib``
```


***В файле  /proc/PID/syscall лежит информация о системных вызовах***

***Также есть файл /proc/763/task/763/status. В однопоточном коде разницы нет. В многопоточном этот файл показывает для каждого потока, отлично от /proc/763***
