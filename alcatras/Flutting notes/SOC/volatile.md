Это инструмент для анализа дампа памяти
```
# 1. Что за образ, какая ОС
vol -f mem.raw windows.info

# 2. Процессы: список и дерево
vol -f mem.raw windows.pslist
vol -f mem.raw windows.pstree

# 3. Скрытые/завершившиеся процессы (сканирование пула)
vol -f mem.raw windows.psscan

# 4. Командные строки — часто палит запуск payload
vol -f mem.raw windows.cmdline

# 5. Сеть
vol -f mem.raw windows.netscan

# 6. Инжекты: RWX-страницы, не привязанные к файлу на диске
vol -f mem.raw windows.malfind

# 7. Модули и DLL процесса
vol -f mem.raw windows.dlllist --pid 4120

# 8. Реестр: hive-список и конкретный ключ
vol -f mem.raw windows.registry.hivelist
vol -f mem.raw windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"

# 9. Извлечение файлов из памяти
vol -f mem.raw windows.filescan
vol -f mem.raw windows.dumpfiles --virtaddr 0x7f8a1c0d2e10

# 10. Дамп процесса целиком
vol -f mem.raw windows.memmap --pid 4120 --dump
```