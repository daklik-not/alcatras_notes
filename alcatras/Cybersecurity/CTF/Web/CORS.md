**Cross-Origin-Resource-Sharing** -  механизм, основанный на HTTP, который ослабляет Secure-Origin-Policy, позволяя загружать данные с источников, где обычно браузер запрещает это.
Также CORS предоставляет механизм *preflight request*, с помощью которого он обращается к серверу, который хостит *cross-origin* ресурсы, чтобы проверить пройдет ли реальный запрос.
CORS используют: *fetch(), XMLHttpRequest, @font-face, drawImage()* и другие
**Simple requests**
В современных спецификациях для сложных запросов(не GET, HEAD, POST с простыми типами и только с разрешенными заголовками и только с разрешенными данными) всегда должен быть prefliight  запрос. c заголовком OPTIONS.
Что можно:
Данные
- `application/x-www-form-urlencoded`
- `multipart/form-data`
- `text/plain`
Заголовки
- Accept
- Accept-Language
- Content-Language
- Content-Type (please note the additional requirements below)
- Range (only with a single range header value; e.g., bytes=256- or bytes=127-255)

**Пример**
```c
const fetchPromise = fetch("https://bar.other");

fetchPromise
  .then((response) => response.json())
  .then((data) => {
    console.log(data);
  });
```
Для этого кода: 
![[Pasted image 20260502202443.png]]
Access-Control-Allow-Origin означает то, что к ресурсу может быть получен доступ от любого источника.
Можно так: *Access-Control-Allow-Origin: https://foo.example*

#### Preflighted requests
Пример запроса, который будет префлайтиться
```c
const fetchPromise = fetch("https://bar.other/doc", {
  method: "POST",
  mode: "cors",
  headers: {
    "Content-Type": "text/xml",
    "X-PINGOTHER": "pingpong",
  },
  body: "<person><name>Arun</name></person>",
});

fetchPromise.then((response) => {
  console.log(response.status);
});
```
Он префлайтится поскольку у него кастомный заголовок, и тело в text/xml
Теперь про то, как будет выглядеть **OPTIONS**
```c
OPTIONS /doc HTTP/1.1
Host: bar.other
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Connection: keep-alive
Origin: https://foo.example
Access-Control-Request-Method: POST //запрос который хотим сделать
Access-Control-Request-Headers: content-type,x-pingother // уведомление о том какие заголовки будут

HTTP/1.1 204 No Content
Date: Mon, 01 Dec 2008 01:15:39 GMT
Server: Apache/2
Access-Control-Allow-Origin: https:/\foo.example // доступ ограничивается только этим доменом
Access-Control-Allow-Methods: POST, GET, OPTIONS // Сервер говорит, что POST и GET валидные методы для запрашивания запроса
Access-Control-Allow-Headers: X-PINGOTHER, Content-Type
Access-Control-Max-Age: 86400 // сколько действует preflight(in sec)
Vary: Accept-Encoding, Origin
Keep-Alive: timeout=2, max=100
Connection: Keep-Alive
```

После этого посылается реальный запрос, каким он изначально посылался

**Перенаправления**
Иногда после OPTIONS приходит redirect. Некоторые браузеры могут отклонить такое перенаправление. Ну там есть какие-то решения, но для КБ они не сильно важны. Если надо - читать на MDN. Вообще лучше просто не допускать 302 на запрос OPTIONS.
Еще предлагается, чтобы сайт, на котором находится пользователь сам реализовал следующую логику. Он отправит простой запрос, который пройдет по редиректам, потом уже OPTIONS на конечный пошлется.

#### Запросы с удостоверением
Удостоверения это cookie, TLS сертификаты, заголовок Authentification, содержащий пароль и логин.
CORS предоставляет возможность создавать запросы с удостоверениям. По умолчанию fetch() не отправляет удостоверения
Надо сделать так:  *const request = new Request(url, { credentials: "include" });*
**Пример**
![[Pasted image 20260502220400.png]]

```
GET /resources/credentialed-content/ HTTP/1.1
Host: bar.other
---стандартные заголовки
Origin: https://foo.example
Cookie: pageAccess=2

HTTP/1.1 200 OK
---стандартные заголовки
Access-Control-Allow-Origin: https://foo.example
Access-Control-Allow-Credentials: true //обязательно иначе будет игнорироваться
Set-Cookie: pageAccess=3; expires=Wed, 31-Dec-2008 01:34:53 GMT

[text/plain content]
```
Вообще сайт к которому мы обращаемся, должен явно указать, что он разрешают сайту на котором мы находимся отправлять запрос.

**Preflight запросы и удостоверения**
CORS префлайты никогда не должны включать удостоверения. Ответ на префлайт должен содержать Access-Control-Allow-Credentials: true

**Запросы с удостоверениями и подстановка**
При ответе на запрос с удостоверением:
1. Сервер не должен использовать \*, для Access-Control-Allow-Origin только явный источник
2. Сервер не должен использовать \* для Access-Control-Allow-Headers только явное указание заголовков
3. Сервер не должен использовать \* для Access-Control-Allow-Methods олько явное указание методовю.
4. Access-Control-Expose-Headers аналогично я устал 1 и то же писать

**Third-Party cookies** #third_party_cookie_cors
Сторонние куки, то есть куки, которые приходят не с того домена на который мы обращаемся, запрещаются браузером и не будут сохранены. Оно конфигурируется в настройках браузера - но это опасно по идее.

#### HTTP заголовки ответов
1. Позволяет источнику можно получить доступ к странице
```c
Access-Control-Allow-Origin: <origin> | * //идет от сервера
```
2. Сервер дает браузеры разрешение на чтение запросов с такими заголовки
```c
Access-Control-Expose-Headers: <header-name>[, <header-name>]*
```
3. Как долго можно без нового префлайта(сколько будет кэширован результат):
```c
Access-Control-Max-Age: <delta-seconds>
```
4.  Позволяет браузеру прочитать запрос с удостоверениями:
   ```c
Access-Control-Allow-Credentials: true
   ```
   5. Методы которые можно использовать(это возврат от префлайта):
```c
Access-Control-Allow-Methods: <method>[, <method>]*
```
6.  Показывает, какие http заголовки могут быть использованы при реальном запросе:
```c
Access-Control-Allow-Headers: <header-name>[, <header-name>]*
```

#### HTTP заголовки запросов
1. Показывает источник отправителя
```c
Origin: <origin> //содержит имя сервера
```
2. Показать в префлайт запросе, какой метод будет в реально запросе
```c
Access-Control-Request-Method: <method>
```
3. Показать какие-то кастомные или сложные заголовки, которые будут использоваться
```c
Access-Control-Request-Headers: <field-name>[,<field-name>]*
```
