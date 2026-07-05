#### HTTP
Компьютер шлет запрос серверу, приложение на сервере работает, сервер возвращает данные.
html - язык разметки.
Код html не совпадает с тем, что отрисовывается, потому что браузер подгружает доп-данные и javascript, который может отрисовать что-то иное. Это называется *initial code*.
Когда браузер обращается к серверу он сначала подгружает html, подгружает картинки ссылки, многопоточно, проверяя нет ли их в кэше. Потом выполняются javaскрипты.
Самая полезная вкладка - network. Preserve log - не очищается панель network при редиректе.
select - выбор, а value то, что будет послано серверу.
XML - формат данных, где данные представлены в виде дерева тегов.
robots.txt - файл который содержит правила для ботов поисковых системах. На CTF часто есть флаги или подсказки.
natas - веб ctf.
Cookie - позволяет одних пользователей отличать от других. Браузер каждый раз шлет сайту cookie, чтобы сайт понимал, что это именно я. Сами куки устанавливает сервер.
GET и POST в принципе ничем не отличаются, только GET можно передавать в URL.
Когда браузер видит параметр SETCOOKIE в запросе он устанавливает их себе в его файлы.
DirBuster - программа для выяснения полной иерархии в дереве.
*Local storage* - те же куки, но доступ к ним имеет все сайты. Там тоже часто флаги.
*Как отправить POST запрос?*
через curl
```c
curl -v --data "name=o@o3.ru&password=o@o3.ru&emaill=o@o3.ru" http://hackyou.ctf.su/register
```

urlencode.org - замена в строке на спецсимволы
--date-urlencode - автоматическая замена в curl

status code позволяет браузеру понять, что делать дальше
код 200 - все хорошо
код 302 - все тоже обработано, но он насильно перейдет по location заголовку
код 404 - страница не найдена.

Можно редактировать заголовок запроса:
```c
Examples:
curl -H "X-First-Name: Joe" https://example.com
curl -H "User-Agent: yes-please/2000" https://example.com
curl -H "Host:" https://example.com
curl -H @headers.txt https://example.com
```

#### Raw-Http
Отправка файлов.

```c raw http
POST /second/level21/ HTTP/1.1
Host: kslweb1.spb.ctf.su
Connection: close
Content-Type: multipart/form-data; boundary=imageBoundary
Content-Length: <точная длина>

--imageBoundary
Content-Disposition: form-data; name="myfile"; filename="shell.php"
Content-Type: image/png

test
--imageBoundary--
```

#### Пример работы с netcut и cookie

```c bash
cookie=votes=1:7bc858c0d521f3bdf696f7187c2da177
for i in {0..17}; do
vote=$(
{
        echo GET /second/level22/ HTTP/1.1
        sleep 1
        echo Connection: close
        sleep 1
        echo Host: kslweb1.spb.ctf.su
        sleep 1
        echo Cookie: $cookie
        sleep 1
        echo
        sleep 1
        echo
} | netcat -C kslweb1.spb.ctf.su 58080 | grep -oE 'votes=[^[:space:]]+'
)
cookie=$vote
echo $cookie
done
```

Если бы не было задержки то подошел бы и netcat в той задаче, но лучше вот так через js

```c
for (var i = 0; i < 1337 ; i++) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://kslweb1.spb.ctf.su/second/level123/', false); // синхронно
    xhr.send();
    var text = xhr.responseText;
    console.log(text);
    document.cookie = text.split("\n")[4].substr(41);
}
```
 