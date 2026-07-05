Aw### Carrier Sense Multiple Access with Collision Avoidance[¶](https://beta.computer-networking.info/syllabus/default/principles/sharing.html#carrier-sense-multiple-access-with-collision-avoidance "Permalink to this headline")
Был разработан для WiFi. Также чувствует канал передачи и избегает коллизии с помощью таймеров. CSMA/CA  использует опознавания. 
CSMA/CA  точно определяет, когда устройство может послать кадр.
 Short Inter Frame Spacing - задержка между получением кадра и отправлением кадра опознавания.
 Distributed Coordination Funciton Inter Frame Space- DIFS  - если прошлый кадр, корректный, то чтобы отправить кадр устройство должно ждать, пока канал будет пустой хотя бы время DIFS.
 Extended Inter Frame Space EIFS  - если предыдущий полученный кадр поврежден, устройство должно освободить канала на EIFS
 $$ SIFS < DIFS < EIFS$$
Возникает проблема с одновременной передачей данных.  Она решается с помощью backoff таймера - рандомная задержка на отправление - как CSMA/CD. Устройство должно регулярно проверять канал, на то, что он свободный - если канал не свободный, то back-off таймер замораживается, до того как канал снова станет свободный.
 ![[Pasted image 20260310181958.png]]
 
# CSMA/CA simplified pseudo-code
```

N=1
while N <= max:
    wait_until(free(channel))
    if correct(last_frame):
        wait(channel_free_during_t >= DIFS)
    else:
        wait(channel_free_during_t >= EIFS)

    backoff_time = int(random(0, min(255, 7 * ( 2 ** (N - 1))))) * slotTime
    wait(channel free during backoff_time)
    # backoff timer is frozen while channel is sensed to be busy
    send(frame)
    wait(ack or timeout)
    if received(ack)
        # frame received correctly
        break
    else:
        # retransmission required
        N = N + 1
else:
    # Too many transmission attempts
```
***Hidden station problem***
Допустим есть 3 хоста, они расположены таким образом что,  Один хост слышит два других хоста, но те 2 хоста друг друга не слышат. Тогда те 2 хоста могу в 1 момент начать передавать на общий хост - будет коллизия.
Чтобы решить это - устройство посылает *RTS- Request To Send* на удаленного получателя, таким образом оно резервирует канал. Он содержит продолжительность запрашиваемой передачи. Получаеть отвечает CTS, который тоже содержит выделенное время. Все хосты, которые могут помешать передаче уведомлены об этом.
![[Pasted image 20260310182025.png]]
