import time 
import psutil
def follow(path, delay=0.1):
    buf = b""
    with open(path , "rb") as f:
        f.seek(0, 2)
        while True:
            chunk = f.read(65536)
            if not chunk: # типо ничего нового, тога поспим
                time.sleep(delay)
                continue
            buf += chunk 
            *lines, buf = buf.split(b"\n")
            # типо разбираем все строки кроме последней
            # * это типо жадный оператор в контексте
            for line in lines:
                yield line.removesuffix(b"\r").decode("utf-8", "replace")


for f in follow("terminated.txt"):
    pid = f.split(" ")[0].split("=")[1]
    pid = int(pid)  # из файла строка, svc.pid() — int
    print(pid)
    