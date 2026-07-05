#### Interrupt-Driven IO
Чтобы процессор не висел в цикле его можно уведомлять с помощью прерываний.  После того как первый символ копируется CPU вызывает планировщик и какой-то другой процесс запускается.  Искомый процесс блокируется.  Когда принтер напечатал символ, он генерирует прерывание. Прерывание останавливает запущенный процесс, запускается обработчик, очищает контроллер прерываний. Это если не используется буферизация
```c
// Исходный код
copy_from_user(buffer, p, count);
enable_interrupts(); 
while (*printer_status_reg != READY);
*printer_data_register = p[0];
scheduler();

// Обработчик прерывания
if (count == 0) {
    unblock_user();
} else {
    *printer_data_register = p[i];
    count = count - 1;
    i = i + 1;
}
acknowledge_interrupt(); //очищение контроллера прерываний.
```
#### IO using DMA
DMA - programmed IO, но без процессора.  Преимущество над interrupt-driven подходом в том, что требуется только 1 прерывание на запуск, и на завершение. Interrupt-driven должен на каждое заполнение буфера вызывать прерывание. Тем не менее DMA значительно медленнее чем процессор -> может не успевать обрабатывать устройство на полной скорости - лучше использовать 
interrupt/programm IO. 
```c
// Код с DMA (Direct Memory Access)
copy_from_user(buffer, p, count);
set_up_DMA_controller();
scheduler();

// Обработчик прерывания от DMA
acknowledge_interrupt();
unblock_user();
return_from_interrupt();
```
