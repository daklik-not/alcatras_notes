Проблема перегрузок решается на транспортном уровне.
TCP использует *AIMD*. 
TCP соединение не может посылать данные быстрее, чем $window / rtt$
Cхема контроля перегрузок основывается на *congestioт* окне. 
1. Окно, которое используется сервером для отправки определяется как $min(cwnd,rwin, swin)$, где *cwnd* это само окно, *rwin* это окно полученное от удаленного хоста, а *swin* это текущее окно отправки.
2. *Additive increase* часть  -  увеличивает окно на MSS байт каждый rtt - *congestion avoidance* *Multiplicative Decrease* - при обнаружении перегрузки, окно делится.

При открытии TCP хост запускается с изначально маленьким окном.
TCP congestion scheme использует *slow start*, чтобы не ждать, пока размер окна станет приемлемым. Во время *slow start* окно перегрузок удваивается каждый rtt.  Slow-start хранит в TCB добавочное значение - *ssthresh*, это последнее значение окна, которое не вызвало перегрузку.

В проводных сетях потери пакетов чаще всего означают перегрузку. В беспроводных это может быть что угодно.

Есть 2 типа перегрузок:
1. *mild congestion* - 3 дублированных сигнала опознавания говорят о легкой перегрузке. Потерянный сегмент отправляется, и если успешно, то TCP делит окно на 2.
 ![[Pasted image 20260527205842.png]]
2. severe congestion - когда таймер перенаправления истекает, сеть считается серьезно загруженной. В этом случае TCP перенаправляет первый потерянный сегмент, устанавливает *threshold* на 50% окна перегрузки, после чего окно скидывается и выполняется медленный старт
![[Pasted image 20260527205752.png]]

***Код TCP congestion control scheme***
```c
# Initialization
cwnd = MSS  # congestion window in bytes
ssthresh= swin # in bytes

# Ack arrival
if tcp.ack > snd.una:  # new ack, no congestion
    if dupacks == 0:  # not currently recovering from loss
        if cwnd < ssthresh:
            # slow-start : quickly increase cwnd
            # double cwnd every rtt
            cwnd = cwnd + MSS
        else:
            # congestion avoidance : slowly increase cwnd
            # increase cwnd by one mss every rtt
            cwnd = cwnd + MSS * (MSS / cwnd)
    else:  # recovering from loss
        cwnd = ssthresh  # deflate cwnd RFC5681
        dupacks = 0
else:  # duplicate or old ack
    if tcp.ack == snd.una:  # duplicate acknowledgment
        dupacks += 1
        if dupacks == 1 or dupacks == 2:
            send_next_unacked_segment  # RFC3042
        if dupacks == 3:
            retransmitsegment(snd.una)
            ssthresh = max(cwnd/2, 2*MSS)
            cwnd = ssthresh
        if dupacks > 3:  # RFC5681
            cwnd = cwnd + MSS  # inflate cwnd
    else:
        # ack for old segment, ignored
        pass

Expiration of the retransmission timer:
    send(snd.una)  # retransmit first lost segment
    sshtresh = max(cwnd/2, 2*MSS)
    cwnd = MSS
```
