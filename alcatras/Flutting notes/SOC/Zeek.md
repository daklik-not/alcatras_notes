Zeek - open-souce коммерческий инструмент мониторинга сети(анализа трафика). Чаще всего не устанавливается на эндпоинты, а на какой-то Linux сервер, который зеркалит весь трафик компании. 
Есть Network Monitoring  - это когда смотрится именно качество сети, доступность устройств и так далее. 
Есть Network Security Monitoring - это когда смотрятся сетевые аномалии  и подозрительные события в  сети.
Zeek предоставляет 50+ логов в 7 категориях.  Zeek дает больше возможностей, чем например Snort.  Короче у Zeek глубина логирования просто больше. 
У Zeek есть:
1. Event Engine - там где обрабатываются пакеты. 
2. Policy Script Interpreter - там где описано, что надо делать с теми или иными пакетами.

![[Pasted image 20261014093106.png]]

У Zeek много фреймворков, которые дополняют его работу.
По умолчанию zek выводит логи в /opt/zeek/logs. 
```
zeek -v // узнать версию линукс
zeekctl status // запущен zeek или нет
zeekctl stop // остановка
zeekctl start // запуск
zeek -C -r sample.pcap // r - прочитать и обработать pcap файл, -C игнорирование ошибок чексумм, -v информация о версии, zeekctl.    
```

***Таблица с типами логов***

| Группа логов                              | Что анализирует и для чего нужна                                                                   | Ключевые файлы логов                                               |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Сетевые протоколы** _(Core)_            | Базовый разбор сетевых сессий на всех уровнях (L4–L7). Показывает общую картину соединений.        | `conn.log`, `dns.log`, `http.log`, `ssl.log`, `dhcp.log`           |
| **Анализ файлов** _(Files)_               | Анализирует файлы в трафике: считает хэши (MD5/SHA256) и изучает структуру PE-файлов (EXE/DLL).    | `files.log`, `pe.log`, `x509.log`, `ocsp.log`                      |
| **Угрозы и детекты** _(Detection)_        | Главный рубеж защиты. Фиксирует аномалии, брутфорс и совпадения с хакерскими базами (IoC).         | `intel.log`, `notice.log`, `signatures.log`, `traceroute.log`      |
| **Сетевая карта** _(Observations)_        | Автоматически составляет живую карту сети: какие хосты активны, какое ПО и версии они используют.  | `software.log`, `known_hosts.log`, `known_services.log`            |
| **Активная защита** _(NetControl)_        | Хроника работы Zeek в режиме IPS: кого он заблокировал на фаерволе, а какой трафик пустил в обход. | `netcontrol_drop.log`, `netcontrol_shunt.log`, `catch_release.log` |
| **Странности и ошибки** _(Miscellaneous)_ | Технический изнаночный слой. Ищет нарушения сетевых стандартов (RFC) и скрытые протоколы.          | `weird.log`, `dpd.log`, `unknown_protocols.log`                    |
| **Диагностика системы** _(Diagnostic)_    | «Пульс» самого Zeek: загруженные скрипты, внутренние ошибки ядра и потеря пакетов (слепота).       | `reporter.log`, `capture_loss.log`, `stats.log`, `print.log`       |
Таблица, которая показывает сколько хранятся те или  иные данные в Zeek

| **Update Frequency** | **Log Name  <br>**   | **Description**                                 |
| -------------------- | -------------------- | ----------------------------------------------- |
| **Daily**            | _known_hosts.log_    | List of hosts that completed TCP handshakes.    |
| **Daily**            | _known_services.log_ | List of services used by hosts.                 |
| **Daily**            | _known_certs.log_    | List of SSL certificates.                       |
| **Daily**            | _software.log_       | List of software used on the network.           |
| **Per Session**      | _notice.log_         | Anomalies detected by Zeek.                     |
| **Per Session**      | _intel.log_          | Traffic contains malicious patterns/indicators. |
| Per Session          | _signatures.log_     | List of triggered signatures.                   |
Написано, что порядок расследования следующий:
1. посмотреть общие сетевые  соединения 
2. найдя что-то подозрительное, смотрим protocol-based логи, связанные с этим
3. посмотреть detection - дополнительные индикаторы
4. посмотреть observation -> увеличить знания о контексте. 

```
cat conn.log | zeek-cut uid proto id.orig_h id.orig_p id.resp_h id.resp_p
// 'вырезаем' поля типо
```

####  Zeek Signatures
Состоит из:
1. Unique name
2. Header filtering, Content filtering
3. Action - создать signature.log файл, например.
Короче это очень похожи на Snort правила, но разница в том, что когда срабатываются Snort правила, то это чаще всего конец, а здесь срабатывание по сигнатуре чаще всего используется дальше в скриптовом движке.
```
zeek -C -r sample.pcap -s sample.sig
//  запустить zeek с сигнатурой
```

Пример сигнатуры:
```
signature http-password {
     ip-proto == tcp
     dst-port == 80
     payload /.*password.*/
     event "Cleartext Password Found!"
}       

signature ftp-admin {
     ip-proto == tcp
     ftp /.*USER.*dmin.*/
     event "FTP Admin Login Attempt!"
}
        
```

Он пишет файлы в *signatures.log* или *notice.log*.

```
cat notice.log | zeek-cut id.orig_h id.resp_h msg
// можно смотреть что и откуда вызвало

cat signatures.log | zeek-cut sub_msg
// точный сетевой контекст
```