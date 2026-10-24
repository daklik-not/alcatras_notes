Ну короче SIEM нужны чтобы осуществлять корреляцию данных, централизацию и иметь доступ к старым логам - например истории местоположений пользователей
***Windows***
 2 источника логов *Windows Event Logs* и *Sysmon*. 
 ```
 // пример правила с sysmon логами для SIEM
 
index=winenv EventCode=3 ComputerName=WINHOST05  
| table _time ComputerName Image SourceIp SourcePort
 ```
У Windows Event Logs нужно использовать:
*Security Logname*
```
index=winenv EventCode=4720 OR EventCode=4722  | table _time EventCode ComputerName Subject_Account_Name
```
*System*
```
// создание сервиса и запуск/остановка событий

index=winenv EventCode=7045 OR EventCode=7036 ComputerName=WINHOST05  
|  table _time EventCode ComputerName
```

***Linux***
*auth.log* - отслеживание активности относящейся к аутентификации.

```
index=linux source="auth.log" *ubuntu* process=sshd | search "Accepted password" OR "Failed password"|
```

*syslog* - события системного уровня
```
index=linux sourcetype=syslog ("CRON" OR "cron")  
|  search ("python" OR "perl" OR "ruby" OR ".sh" OR "bash" OR "nc")

// seach работат как доп фильтрация
```

***Web-Server***
Самые полезные логи - **access logs** и ***error logs***. 
Сложный Splunk запрос для поиска брут-форс атаки
```
index=* method=POST uri_path="/wp-login.php"  
| bin _time span=5m  # bin _time span=5m - округление до 5m
| stats values(referer_domain) as referer_domain values(status) as status values(useragent) as UserAgent values(uri_path) as uri_path count by clientip _time  
| where count > 25  
| table referer_domain clientip UserAgent uri_path count status
```
Splunk фильтр для поиска веб-шелла:
```
index=*  
| search status=200 AND uri_path IN(*.php, *.phtm, *.asp, *.aspx, *.jsp, *.exe) AND (method=POST AND method=GET)  
| stats values(status) as status values(useragent) as UserAgent values(method) as method  
  values(uri) as uri values(clientip) as clientip count by referer_domain  
| where count > 2  
| table referer_domain count method status clientip UserAgent uri
```
Splunk фильтр для поиска DDos атаки:
```
index=* status=503  
| bin _time span=10m  
| stats values(referer_domain) as referer_domain values(status) as status values(useragent) as UserAgent values(uri_path) as uri_path count by clientip _time  
| where count > 100000  
| table _time referer_domain clientip UserAgent uri_path count status
```
# Alert Triage With Splunk
Splunk регулярки:
```
^\d{4}-\d{2}-\d{2}T[^\s]+\s+(?<log_hostname>\S+)
// Обьяснение:
	^ - символ начала строки
	\d{4} - 4 любых цифры
	[^\s]+ - 1 или более символов(+), которые не являются([^]) пробелами \s
	\s+ - 1 или более пробельных символов
	(?<log_hostname>\S+) - имен. группа захв(?<log_hostname>) \S+ непроб символы
	
(?: invalid user)? - неименованная группа

// Пример использования:
index="linux-alert"
| rex "sshd\[\d{1,6}\]:\s*(?<result>Failed password|Accepted password)\s+for\s+(?<username>\S+)" 
| search username="john.smith" result="Failed password"
// пример моей регулярки для извлечения пользователя и результата авторизации
```

# Alert Triage With Elastic
Пример работы с эластиком: 
```
_index:weblogs and url.path : *cmd*

@timestamp >= "2025-07-20T05:11:22" and winlog.event_id:4624 and host.name:winserv2019.some.corp and winlog.event_data.TargetUserName:Administrator
```