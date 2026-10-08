

Sysmon дает очень подробную информацию о создании процессов, сетевых соединениях и изменениях файлов на Windows. 
Sysmin требует config-file, чтобы понять как анализировать те события, которые он получает. 


Пример правила в конфиг-файле: 
```
<RuleGroup name="" groupRelation="or">  
<ProcessCreate onmatch="exclude">  
  <CommandLine condition="is">C:\Windows\system32\svchost.exe -k appmodel -p -s camsvc</CommandLine>  
</ProcessCreate>  
</RuleGroup>
```
#### Самые важные Event ID
1. Event ID 1: Создание процесса
2. Event ID 3: Сетевое соединения
3. Event ID 7: Загрузка DLL библиотеки
4. Event ID 8: Создание удаленного потока
5. Event ID 11: Создание файла
6. Event ID 12, 13, 14 - изменения или модификации регистра
7. Event ID 15 - файлы созданные в альтернативном потоке данных
8. Event ID 22 DNS event - логирование всех DNS запроосов

#### Установка
```
choco install sysinternals -y // удобная установка через chocolatey
Sysmon.exe -i C:\Users\0987a\Configurations\sysmon-config.xml
```

#### Best Practices
1. Exclude > Include.
2.  Использование CLI для подробного поиска и фильтрации
3. Знать свою среду


#### Metasploit
Может запускать эксплойты на машине, и создавать C2 с помощью *meterpreter shell*. 
Здесь мы будет искать как раз-таки этот шелл. Подозрительные порты 4444, 5555(хотя в реальном поиске их легко можно поменять, так что на них лучше не надеяться). 
```
//типо смотрим сетевые соединения на этих портах
<RuleGroup name="" groupRelation="or">  
	<NetworkConnect onmatch="include">  
		<DestinationPort condition="is">4444</DestinationPort>  
		<DestinationPort condition="is">5555</DestinationPort>  
	</NetworkConnect>  
</RuleGroup>
```
Но вообще это все бред и на практике так его не ищут. Смотрят, например так:
```
<RuleGroup name="Webserver Spawning Shell" groupRelation="and">
  <ProcessCreate onmatch="include">
    <ParentImage condition="end with">\w3wp.exe</ParentImage>
    <ParentImage condition="end with">\nginx.exe</ParentImage>
    <ParentImage condition="end with">\httpd.exe</ParentImage>
    <Image condition="end with">\cmd.exe</Image>
    <!-- Если родитель веб-сервер, а ребенок консоль — это 100% взлом -->
  </ProcessCreate>
</RuleGroup>

```
или вот так
```
Оригинальный svchost живет только в System32
<RuleGroup name="Process Masquerading" groupRelation="and">
  <ProcessCreate onmatch="include">
    <Image condition="contains">svchost.exe</Image>
  </ProcessCreate>
  <ProcessCreate onmatch="exclude">
    <Image condition="begin with">C:\Windows\System32\</Image>
  </ProcessCreate>
</RuleGroup>
```

#### Mimikatz
#vsm
mimikatz - используется для дампа lsass. С появлением Windows11 это немного устарело, поскольку у процесса lsass де-факто больше нет доступа к доменным учеткам - они вынесены в lsasio и даже при **SYSTEM** доступе нельзя явно прочитать.  Тем не менее он все еще используется. Например локальные учетные записи устройства также находятся в lsass.

Чтобы искать mimikatz нужно смотреть на странное lsass поведение. Для этого используется EventID ProcessAcess(10). Оно регистрирует попытки одного процесса открыть другой процесс для чтения или записи его памяти.

Если доступ к LSASS осуществляется через процесс отличный от svchost это подозрительно и должно расследоваться.
```
// то есть исключаем все svchost, но все остальное подозритльно
<RuleGroup name="" groupRelation="or">  
	<ProcessAccess onmatch="exclude">  
		<SourceImage condition="image">svchost.exe</SourceImage>  
	</ProcessAccess>  
	<ProcessAccess onmatch="include">  
		<TargetImage condition="image">lsass.exe</TargetImage>  
	</ProcessAccess>  
</RuleGroup>
```

#### Hunting malware
RAT - remote access trojan.  Пользователь скачивает файл из интернета, после чего злоумышленник получает полный контроль над чужим компьютером. 
Для обнаружения Rat и C2 будем смотреть подозрительные порты вроде 1034 и 1604, исключая стандартный события. 
____
[Malware Back Connect Ports - Google Таблицы](https://docs.google.com/spreadsheets/d/17pSTDNpa0sf6pHeRhusvWG6rThciE8CsXTSlDUAZDyo/edit?pli=1&gid=0#gid=0)
Важно. Сам по себе порт не является доказательством чего-либо. Злоумышленник может легко поменять порт в коде программы, перекомпилировать его - и обойти средства защиты построенные на порте.  Но, порт является в первую очередь признаком, ради которого стоит присмотреться. Насколько я понял. Большинство малварей - это массовое распространение одного и того же кода -> порт не меняется. Поэтому стоит обращать на это внимаени
____
Пример правила на поиск RAT:
```
<RuleGroup name="" groupRelation="or">  
	<NetworkConnect onmatch="include">  
		<DestinationPort condition="is">1034</DestinationPort>  
		<DestinationPort condition="is">1604</DestinationPort>  
	</NetworkConnect>  
	<NetworkConnect onmatch="exclude">  
		<Image condition="image">OneDrive.exe</Image>  
	</NetworkConnect>  
</RuleGroup>
```

#### Persistence 
Есть множество способов, как можно установить *persistence*. Здесь будут рассматриваться пример с FileCreation и RegistryModification
Например что-то вот такое:
```
//Созданиее файлов .exe и других в startup - подозрительон
<RuleGroup name="" groupRelation="or">
  <FileCreate onmatch="include">
    <TargetFilename name="T1547.001" condition="contains">\Microsoft\Windows\Start Menu\Programs\Startup\</TargetFilename>
  </FileCreate>
  <FileCreate onmatch="exclude">
    <TargetFilename condition="end with">.lnk</TargetFilename>
    <TargetFilename condition="end with">.url</TargetFilename>
  </FileCreate>
</RuleGroup>
```
Или изменения в политике регистра, которые тоже указывают на автозапуск
```
<RuleGroup name="" groupRelation="or">  
	<RegistryEvent onmatch="include">  
		<TargetObject name="T1060,RunKey" condition="contains">CurrentVersion\Run</TargetObject>  
		<TargetObject name="T1484" condition="contains">Group Policy\Scripts</TargetObject>  
		<TargetObject name="T1060" condition="contains">CurrentVersion\Windows\Run</TargetObject>  
	</RegistryEvent>  
</RuleGroup>
```

#### Windows Evasion Techniques
#windows_evasion_techniques
 1. Alternate Data Streams - в Windows у каждого файла есть скрытые дополнительные потоки, которые обычный Dir не показывает. При этом поток не увеличивает размер файла.
2.  Injections - открыть чужой процесс(OpenProcess) выделить в нем память(VirtualAllocEx), записать свой код(WriteProcessMemory). Далее можно заставить процесс выполнить CreateRemoteThread. 
 3.  Masquerading - Процесс притворяется кем-то другим. Например svch0st.exe вместо svchost.exe, или svchost не в System32. 
 4. Packing/Compression - исходный exe шифруется и превращается в массив упакованных данных.  Далее этот массив упакованных данных записывается в новый exe, после чего в начало этого exe добавляется маленький загрузчик. Когда скачанный файл выполняется, загрузчик расшифровывает exe файл, и запускает исходную программу. 
 5. Recompiling - перекомпилировать исходный код инструмента, при этом добавить что-то еще, чтобы было бинарное другое - защита от сигнатурного детекта по хэшу файла. 
 6. Obfuscation - намеренное усложнение кода, чтобы автоматике или человеку было тяжелее читать. Например записать команды в base64
 7. Anti-Reversing Techniques - программа не дает себя изучать, например может проверять запущена ли она на виртуальной машине, или в песочнице. 

Здесь будет про ADS  и Injections
чтобы отобразить файлы с потоками надо использовать:
```
Get-Item * -Stream *
```
Пример sysmon правила для мониторинга создания ADS. 
```
<RuleGroup name="Monitor_ADS_Creation" groupRelation="or">
  <FileCreateStreamHash onmatch="include">
    <TargetFilename condition="contains">Downloads</TargetFilename>
    <TargetFilename condition="contains">Temp\7z</TargetFilename>
    <!-- Ищет расширение .hta перед объявлением потока -->
    <TargetFilename condition="contains">.hta:</TargetFilename> 
    <!-- Ищет расширение .bat перед объявлением потока -->
    <TargetFilename condition="contains">.bat:</TargetFilename> 
  </FileCreateStreamHash>
</RuleGroup>
```
Например может быть что-то вот такое:
```
<RuleGroup name="" groupRelation="or">  
	<CreateRemoteThread onmatch="exclude">  
		<SourceImage condition="is">C:\Windows\system32\svchost.exe</SourceImage>  
		<TargetImage condition="is">C:\Program Files (x86)\Google\Chrome\Application\chrome.exe</TargetImage>  
	</CreateRemoteThread>  
</RuleGroup>
```

Больше примеров работы с логами sysmon:
```
Get-WinEvent -Path "C:\Users\0987a\Configurations\Investigation-1.evtx" -FilterXPath "*/System/EventID=13 or */System/EventID=12 or */System/EventID=14" 
// вытащить все что связано с реестром

```