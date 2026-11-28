# /// script
# requires-python = ">=3.10"
# dependencies = ["scapy", "cryptography"]
# ///

import random
from collections import Counter
import math
import os
from pathlib import Path


threshold = 2

def calc_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def calc_file_entropy(filename):
    f_size = os.path.getsize(filename)
    with open(filename, "r+b") as f:
        data_for_entropy = bytearray()
        indexes = [random.randint(0, f_size - 1) for i in range(10)]
        for ind in indexes:
            f.seek(ind, 0) # это от начала
            ent_dat = f.read(65536)
            data_for_entropy += ent_dat
        file_entropy = calc_entropy(data_for_entropy)
        if file_entropy > threshold:
            print(f"Potentially enc. file: {filename, file_entropy}")

def checkFiles(directory):
    files = [p for p in directory.rglob("*") if p.is_file()]
    for f_name in files:
        calc_file_entropy(f_name)


directory = Path(__file__).resolve().parent / "EncryptedFiles"

checkFiles(directory)
