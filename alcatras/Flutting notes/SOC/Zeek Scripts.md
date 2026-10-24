У Zeek есть свой скриптовый язык. 
У него есть установленные по умолчанию скрипты  /opt/zeek/share/zeek/base
Пользовательские скрипты следует сохранять сюда /opt/zeek/share/zeek/site
Policy scripts также следует класть /opt/zeek/share/zeek/policy
Чтобы Zeek запускал скрипты нужно менять его конфигурационный файл:
/opt/zeek/share/zeek/site/local.zeek
У скриптов .zeek расширение.
load @/script/path, load @script-name - это команды с помощью которых можно дозагружать скрипты в ливе. 
Преимущество консольных скриптов в том, что можно легко передавать информацию в другие инструменты. 
```
zeek -C -r sample.pcap 101.zeek
// запуск zeek со скриптом 
```
Пример Zeek скрипта:
```
event dhcp_message (c: connection, is_orig: bool, msg: DHCP::Msg, options: DHCP::Options)
{
print options$host_name;
}
   
// event - обьявление обработчика событий 
// dhcp_message - встроенное в zeek событие - слушает сетевой трафик и срабатывает каждый раз, когда перехватывается DHCP пакет. 
// c: connection  - вся информация о сетевом соединении
// is_orig: bool - кто отправил пакет(типо 1 - 0, клиент или сервер)
// msg - технические параметры DHCP сообщения
// options - структура со всеми DHCP опциями 
// $ - обращение к конкретному полю структуры.

```
Еще пример
```
event zeek_init()
    {
     print ("Started Zeek!");
    }
event zeek_done()
    {
    print ("Stopped Zeek!");
    }

# zeek_init: делается только когда zeek запускает свой процесс
# zeek_done: делается только когда zeek завершает свой процесс 
# print: вывод сообщение на экран 


event new_connection(c: connection) { print c; }
// вывод сырых данных

print fmt ("Source Host: %s # %s --->", c$id$orig_h, c$id$orig_p);
// встраивание переменных в строки
```

#### scripts and signatures together 
```
zeek -C -r ftp.pcap local
// запускает zeek вместе со всем что указано в 
local.zeep(/usr/local/zeek/share/zeek/site/local.zeek)

zeek -C -r ftp.pcap /opt/zeek/share/zeek/policy/protocols/ftp/detect-bruteforcing.zeek
// запуск с явным указанием скрипта 
```

#### zeek scripts frameworks
В Zeek есть много фреймворков, которые помогают изучать различные события. 
***File Framework hashes***
```
@load /opt/zeek/share/zeek/policy/frameworks/files/hash-all-files.zeek
// загрузить в оперативную память процесса zeek весь нужный код      
```
Пример:
```
ubuntu@ubuntu$ cat /opt/zeek/share/zeek/policy/frameworks/files/hash-all-files.zeek 
# Enable MD5, SHA1 and SHA256 hashing for all files.

@load base/files/hash
event file_new(f: fa_file)
	{
	Files::add_analyzer(f, Files::ANALYZER_MD5);
	Files::add_analyzer(f, Files::ANALYZER_SHA1);
	Files::add_analyzer(f, Files::ANALYZER_SHA256);
	// ну короче добавляем к f, которая является структурой со всеми данными 
	поля из фреймворка. 
}     
```

***File Framework - Extract files***
```
zeek -C -r case1.pcap /opt/zeek/share/zeek/policy/frameworks/files/extract-all-files.zeek
// выделение всех файлов из pcap файла - попадает в папке extract_files

file *| nl
// не zeek но полезно знать как залистить файлы 

cat files.log | zeek-cut fuid conn_uids tx_hosts rx_hosts mime_type extracted | nl
// какие поля можно извлечь

grep -rin CZruIO2cqspVhLuAO9 * | column -t | nl | less -S
// -r рекурсивно ищет во всех подпапках
// -i игнорировать регистр
// -n выводить номер строки в файл
//  * искать во всех файлах текущей папки
//  column -t  выводит текст в красивые колонки
// less -S не все + перенос остатка строки 
```
***Notice Frameworks | Intelligence***
Этому фреймворку нужны фиды(которые TI фиды), 
/opt/zeek/intel/zeek_intel.txt - например файлы можно хранить вот тут


#### zeek scripts packages
У Zeek есть свои плагины. Они содержат скрипты автоматизации(.zeek), описания новых протоколов(.spicy),

| zkg install package_path/git_url | установить пакет           |
| -------------------------------- | -------------------------- |
| `zkg list`                       | залистить установл. пакеты |
| `zkg remove`                     | удалить пакет              |
| `zkg refresh`                    | посмотреть обновления      |
| `zkg upgrade`                    | обновить пакеты            |
Чаще всего пакет загружается из скрипта. 
Типо вот так вот:
```
cat sniff-demo.zeek 
// вывод: @load /opt/zeek/share/zeek/site/zeek-sniffpass

zeek -Cr http.pcap /opt/zeek/share/zeek/site/zeek-sniffpass
// можно так

zeek -Cr http.pcap zeek-sniffpass
// или так
```
