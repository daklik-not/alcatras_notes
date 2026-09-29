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