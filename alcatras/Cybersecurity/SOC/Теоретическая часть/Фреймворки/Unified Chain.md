Фреймворк, устанавливающий фазы атаки и риски.
*Kill chain* - термин, который используется для описания этапов атак.
**Thread Modeling**
Набор шагов чтобы значительно улучшить безопасность системы. Для оценки безопасности системы используются методологии *STRIDE*, *DREAD*, *CVSS*.
На картинке представлена сама цепочка:
![[Cache/Pasted image 20260612150526.png]]
*Lateral movement* - перемещение между машинами, например с компьютера мененджера на компьютер системного аналитика.
#### IN
![[Cache/Pasted image 20260612164042.png]]
**Reconnaissance ([MITRE Tactic TA0043(opens in new tab)](https://attack.mitre.org/tactics/TA0043/))**
Изучение, какие системы и сервисы запущены на цели, найти список работников, которых можно эксплуатировать в рамках социальной инженерии, поиск аутентификационных данных.
**Weaponization ([MITRE Tactic TA0001(opens in new tab)](https://attack.mitre.org/tactics/TA0001/))**
Настройка инфраструктуры для выполнения атаки
**Social Engineering ([MITRE Tactic TA0001(opens in new tab)](https://attack.mitre.org/tactics/TA0001/))**
Манипуляция работников с целью выполнения ими действий, которые приведут к последующей атаке.
**Exploitation ([MITRE Tactic TA0002(opens in new tab)](https://attack.mitre.org/tactics/TA0002/))**
Использование уязвимостей системы для выполнения кода.
**Persistence ([MITRE Tactic TA0003(opens in new tab)](https://attack.mitre.org/tactics/TA0003/))**
Техника, для реализации постоянного доступа к системею
**Defence Evasion ([MITRE Tactic TA0005(opens in new tab)](https://attack.mitre.org/tactics/TA0005/))**
Как именно злоумышленник обходит средства защиты, например, файрволлы. Эта фаза дает информацию о том, как улучшить их системы защиты.
**Command & Control ([MITRE Tactic TA0011(opens in new tab)](https://attack.mitre.org/tactics/TA0011/))**
Установление соединения между злоумышленником и системой.
**Pivoting ([MITRE Tactic TA0008(opens in new tab)](https://attack.mitre.org/tactics/TA0008/))**
Техника, используемая для получения доступа к устройствам в локальной сети, к которой нет доступа из глобальной.

#### Through
Следует после IN, то есть первичного проникновения. Атакующий настроит базу на одной из систем, которая будет вести себя как *pivot* точка. На картинке индивидуальная фаза атаки ""Through"".
![[Cache/Pasted image 20260612171316.png]]
#### Pivoting ([MITRE Tactic TA0008(opens in new tab)](https://attack.mitre.org/tactics/TA0008/))
Когда атакующий получает доступ к какой-либо системе, далее они используют ее в последующих стадиях, как точки распределения.
#### Discovery ([MITRE Tactic TA0007(opens in new tab)](https://attack.mitre.org/tactics/TA0007/))
Поиск информации о системе, но уже с более большим уровнем доступа.
#### Privilege Escalation ([MITRE Tactic TA0004(opens in new tab)](https://attack.mitre.org/tactics/TA0004/))
Злоумышленник попытается получить больше привилегий в системе.
#### Execution([MITRE Tactic TA0002(opens in new tab)](https://attack.mitre.org/tactics/TA0002/))
 Деплой(настройка, размещение, запуска) вредоносного кода - удаленные Трояны, C2 скрипты.
#### Credential Access ([MITRE Tactic TA0006(opens in new tab)](https://attack.mitre.org/tactics/TA0006/))
 Злоумышленник попробует украсть учетные данные пользователей - это позволит повысить привилегии и дольше оставаться незамеченным.
#### Lateral Movement([MITRE Tactic TA0008(opens in new tab)](https://attack.mitre.org/tactics/TA0008/))
Злоумышленник попытается прыгнуть на другу систему.

#### OUT
Действия направлены на подрыв ***CIA TRIAD - confidentially, integrity(целостность), доступность***. 
![[Cache/Pasted image 20260612173253.png]]


#### **Collection** ([MITRE Tactic TA0009(opens in new tab)](https://attack.mitre.org/tactics/TA0009/))
Злоумышленник собирает все доступные данные.
#### **Exfiltration** ([MITRE Tactic TA0010(opens in new tab)](https://attack.mitre.org/tactics/TA0010/))
Данные воруются, при отправке они шифруются, чтобы было сложно их обнаружить
#### **Impact** ([MITRE Tactic TA0040(opens in new tab)](https://attack.mitre.org/tactics/TA0040/))
Злоумышленник компроментирует доступность и целостность данных

#### **Objectives**
Злоумышленник добивается цели, например, получает деньги от компании














