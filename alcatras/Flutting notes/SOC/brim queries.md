В Brim Zui запросы(**queries**) это способ поиска фильтрации и анализа данных.
Есть заранее установленные queries, но в Zui их нет - они лежат вот тут:
[brimcap/queries.json at main · brimdata/brimcap · GitHub](https://github.com/brimdata/brimcap/blob/main/queries.json)

***custom queries***
```
10.0.0.1 AND some_string
// просто поиск строки и численного значения

id.orig_h == 192.168.121.40
// фильт на значение поля

_path=="conn"
// все из conn log файла

_path=="conn" | cut id.orig_h, id.resp_p, id.resp_h | sort | uniq
// cut как zeek-cut работает типо
```
Brim плохо ищет по тупым строкам, поэтому лучше всего искать по специальным полям. 
#### Полезные запросы
```
_path=="conn" | cut id.orig_h, id.resp_h, id.resp_p, service | sort id.resp_p | uniq -c | sort -r
// позволяет посмотреть все взаимодействующие хосты в сети. Если добавить uniq -c и sort -r, то увидим какие хосты чаще всего взаимодействуют между собой и по каким портам 

_path=="conn" | cut id.orig_h, id.resp_p, id.resp_h, duration | sort -r duration
// важно смотреть на длительность соединения 

_path="conn" | put total_bytes := orig_bytes + resp_bytes | sort -r total_bytes | cut uid, id, orig_bytes, resp_bytes, total_bytes
// позволяет смотреть на количество передаваемых байтов.  Очевидно, что если клиент передает сравнимое с файловым сервером количество это не очень хорошо

_path=="dns" | count () by query | sort -r
_path=="http" | count () by uri | sort -r
// нужно смотреть DNS и HTTP запросы с целью поиска C2 серверов. 

_path=="dhcp" | cut host_name, domain
// с помощью DCPC логов можно найти подозрительные хосты в сети.


_path=="conn" | put classnet := network_of(id.resp_h) | cut classnet | count() by classnet | sort -r
// network_of() возвращает сеть IP адреса. Это нужно чтобы можно было группировать когда много мелких IP адресов обращаются.  

filename!=null
// поиск файлов. Позволяет искать подозрительные файлы 

_path=="dce_rpc" OR _path=="smb_mapping" OR _path=="smb_files"
// смотрим dce_rpc(вызов удаленных процедур на Windows,
// smb_mapping - подллючение к сетевым ресурса
// smb_files - операциии с файлами внутри smb шар

 event_type=="alert" or _path=="notice" or _path=="signatures"
 // смотрим алерты и сигнатуры, которые сработали. 
```