
*Persistent CSMA*
Пусть хосты слушают каналы - если канал пустой, то можно отправлять кадр. Коллизии происходят, когда два терминала слушают канал одновременно и как только он становится свободен посылают сообщение.
#### persistent CSMA
```

N = 1
while N <= max:
    wait(channel_becomes_free)
    send(frame)
    wait(ack or timeout)
    if ack:
       break  # transmission was successful
    else:
             # timeout
             N = N + 1
else:
    # Too many transmission attempts
```
*Non persistent CSMA*
Он не слушает канал постоянно(*busy waiting*). Он засыпает на какое-то время, когда канал не свободен - это улучшает утилизацию. Неперсистентый CSMA из-за задержки дольше.

```
N = 1
while N <= max:
    listen(channel)
    if free(channel):
        send(frame)
        wait(ack or timeout)
        if received(ack):
           break  # transmission was successful
        else:
                 # timeout
                 N = N + 1
    else:
        wait(random_time)
else:
    # Too many transmission attempts
```