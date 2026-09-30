Система логирования на Linux называется syslog.  Фактически это просто текстовые файлы. 
Вообще по умолчанию очень много логов отключено
На Windows  это не текстовые файлы, однако с помощью WinAPI их можно перевести в XML.  Их формат .ext | .evtx (лежат вот здесь C:\Windows\System32\winevt\Logs). 
Есть 3 способа получения логов
1. Event Viewer ( eventvwr.msc - запуск из консоли).  Графический редактор для просмотра логов. Там все достаточно интуитивно понятно, поэтому расписывать особо смысла не вижу. 

***wevutil.exe***
инструмент командной строки для извлечения логов. 
```
wevtutil cl - признак очищения логов
wevtutil.exe gl Microsoft-Windows-PowerShell/Admin - получить лог
wevtutil.exe --help - help файл
```
***Get-WinEvent***
Рекомендуется фильтровать таким образом, а не через Where-Object
```c
Get-WinEvent -FilterHashtable @{
	LogName='Application' 
	ProviderName='WLMS' 
	ID=11707
} -MaxEvents 10
```
-FIlterHashTable не рекомендуется использовать не на стандартных логха

***XPath filtering***
![[Pasted image 20260928233554.png]]
```
Get-WinEvent -LogName Application -FilterXPath '*/System/EventID=100'

или так

wevtutil.exe qe Application /q:*/System[EventID=16394] /f:text /c:2
где /f:text это представление в виде текста, а /c:2 это сколько выводим ивентов
```

![[Pasted image 20260928234208.png]]
```
Get-WinEvent -LogName Application -FilterXPath "*/System/Provider[@Name='Microsoft-Windows-Security-SPP']"
```

Можно комбинировать несколько фильтров:
```
Get-WinEvent -LogName Application -FilterXPath '*/System/EventID=101 and */System/Provider[@Name="WLMS"]'
```
Для Data что то вот такое:
```
Get-WinEvent  -LogName Security -FilterXPath '*/EventData/Data[@Name="SubjectUserSid"]="S-1-5-18"'
```

#### Event ID
```
Security log
eventID=4642 // success logon
eventID=4625 // failed logon
eventID=4738 // user account change
eventID=7045 // service installed
eventID=4725 // user account change
```
[[EventID Reference.canvas]]
[Windows Security Log Encyclopedia](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/default.aspx?i=j) - почти все что связано с безопасностью
[Some security staff also](https://web.archive.org/web/20190115215749/https://apps.nsa.gov/iaarchive/customcf/openAttachment.cfm?FilePath=/iad/library/ia-guidance/security-configuration/applications/assets/public/upload/Spotting-the-Adversary-with-Windows-Event-Log-Monitoring.pdf&WpKes=aF6woL7fQp3dJiqyJL2LenrLxuHC7ztGtVNK3x)
