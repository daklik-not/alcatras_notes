# /// script
# requires-python = ">=3.10"
# dependencies = ["scipy", "scapy", "pandas"]
# ///

from scapy.all import *
from scipy.stats import entropy
from collections import Counter
import math

# тут был pandas, но он очень медленный для разбора pcap поэтому я просто
# навайбкодил свою энтропию
def calc_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())

'''
Немного про энтропию. Это то что оценивает рандомность. Она считается или через 
наты или через биты
Всего 256 байт, значит чтобы угадать следующий, максимальная энтропия:
Через биты: 1 / 8 то есть угадать 8 битов (base = 2)
Через наты: ln(256)
короче там в этой энтропии шеннона есть логарифм у которого меняется основание
'''

entropyThreshold = 2.5
def processPayloads(p):
    if not p.haslayer(Raw):
        return
    load = p[Raw].load
    e = calc_entropy(load)
    if e >= entropyThreshold and len(load) % 16 == 0:
        # len(load) % 16 == 0, очень грубый фильтр отсеиватель
        # http запрос тоже может быть такой длинйо
        print(f"Potentially encr. data: {load.hex()}")
    return

sniff(offline="some.pcapng", prn=processPayloads, filter="tcp")