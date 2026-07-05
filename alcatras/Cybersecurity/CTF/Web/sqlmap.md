Для GET запроса
```c
sqlmap -u адрес_сайта
`sqlmap -u http://www.dwib.org/faq2.php?id=8 - это типо get
sqlmap -u "google.com" --data="query=1" --level=3 --dump --batch - это типо POST

```