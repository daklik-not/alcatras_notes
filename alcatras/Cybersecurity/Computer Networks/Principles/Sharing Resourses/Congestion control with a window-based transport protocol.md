### Congestion control with a window-based transport protocol
В надежных транспортных протоколах альтернатива в том, чтобы динамически регулировать *sending window*. Это используется в TCP и SCTP.
Максимально возможная скорость передачи это $window / rtt$, где window это размер окна, а rtt - round-trip-time.
Чтобы регулировать скорость передачи используется *congestion window*. Это окно перегрузок ограничивает *sending window* - $window = min(swin, cwin)$. 

```
cwin = 1  # congestion window measured in segments
# Ack arrival
if ack_received:
    if newack:  # new ack, no congestion
        # increase cwin by one every rtt
        cwin = cwin + (1/cwin) // типо увеличение на 1 сегмент
        // почему так работает хз
    else:
        # no increase

if congestion_detected:
    cwin = cwin / 2 # only once per rtt
```
Пример работы с *sending window*  - \* - пакеты с перегрузкой
![[Cache/Pasted image 20260310182331.png]]
Пример для нескольких хостов и 1 роутера
![[Cache/Pasted image 20260310182341.png]]
____