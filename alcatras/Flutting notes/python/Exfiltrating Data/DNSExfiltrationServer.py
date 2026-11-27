# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy"]
# ///

from scapy.all import *
import socket

from base64 import b64decode
from time import sleep

port = 13337

# переменная вынесена на уровень модуля, чтобы global extracted работал
extracted = ""


def sendResponse(x, response_ip):
    question = x[DNS].qd
    # Answer в секции qd
    # ttl клиент закэщирует ответ на 1000 секунд
    # rdata - полезные данные овета, rrname - имя запрашиваемого доменв
    answer = DNSRR(rrname = question.qname, ttl = 1000, rdata = response_ip)
    ip = IP(src = x[IP].dst, dst = x[IP].src)
    dns = DNS(
        id = x[DNS].id,  # уникальый идентификатор, нужен для сопоставления
        qr = 1, # показываем что это ответ
        qdcount = 1, # прочитать несколько вопросов
        ancount = 1, # можно возвращать несколько ответов
        qd = x[DNS].qd,
        an = answer
        # если несколько то answer1 / answer2
    )
    if x.haslayer(UDP):
        udp = UDP(dport = x[UDP].sport, sport = port)
        response = ip / udp / dns
    elif x.haslayer(TCP):
        tcp = TCP(dport = x[TCP].sport, sport = port)
        response = ip / tcp / dns
    else:
        return
    send(response, verbose = 0)


def extractData(x):
    global extracted
    # когда DNS сервер недоступен сервер отвечает notreachable ICMP
    # мы не хотим это ловить
    if not (x.haslayer(DNS) and not x.haslayer(ICMP)):
        return

    # проверки UDP и TCP разделены, чтобы не обращаться к несуществующему слою
    if x.haslayer(UDP):
        if x[UDP].dport != port:
            return
    elif x.haslayer(TCP):
        if x[TCP].dport != port:
            return
    else:
        return

    domain = x[DNS].qd.qname
    # индекс первое вхождение указанного элемента в последовательности
    ind = domain.index(bytes(".", "utf-8"))
    data = domain[:ind]
    padnum = ((4 - len(data) % 4)) % 4
    data += bytes("=" * padnum, "utf-8")
    try:
        decoded = b64decode(data).decode("utf-8")
        print(f"Recieved: {decoded}")
        if decoded == "R": # типо говорим что коцне
            sendResponse(x, "10.0.0.2")
            print("End transmission")
            print(extracted)
            extracted = ""  # сбрасываем, чтобы данные не копились между сессиями
        else:
            extracted += decoded
            sendResponse(x, "10.0.0.1")
    except Exception as e:
        print(e)
        sendResponse(x, "10.0.0.0")

sniff(iface = "lo", prn = extractData)