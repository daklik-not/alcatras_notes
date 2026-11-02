import xml.etree.ElementTree as ET
import psutil, datetime, pywintypes, win32evtlog, dateutil, hashlib

logtype = "Microsoft-Windows-WMI-Activity/Trace"
flags = win32evtlog.EvtQueryForwardDirection
query = "*[System[EventID=23]]"

ERROR_NO_MORE_ITEMS = 259
EvtRenderEventXml = getattr(win32evtlog, "EvtRenderEventXml", 1)

def sha256_file(path):
    # hashlib в стандартной либе
    # rb - read binary i guess
    with open(path, "rb") as f:
        # file_digest чтение файлов, hexdigest превращает в хэш
        return hashlib.file_digest(f, "sha256").hexdigest() 

def GetEventLogs(logtype, flags, query="*"):
    q = win32evtlog.EvtQuery(logtype, flags, query)
    events = []
    try:
        while True:
            try:
                batch = win32evtlog.EvtNext(q, 100, 0)
            except pywintypes.error as err:
                if err.winerror == ERROR_NO_MORE_ITEMS:
                    break
                raise
            if not batch:
                break
            events.extend(batch)
            print(f"Прочитано {len(batch)} событий (всего {len(events)})")
    finally:
        q.Close()          # PyEVT_HANDLE закрывается методом .Close()
    return events


def ParseEvents(events):
    print(f"Начинаю разбор {len(events)} событий")
    path = "./{*}UserData/{*}ProcessCreate/{*}"
    path_system = "./{*}System"
    for event in events:
        try:
            xml = win32evtlog.EvtRender(event, EvtRenderEventXml)
            root = ET.fromstring(xml)
            name = root.findtext(path + "Commandline")
            pid = root.findtext(path + "CreatedProcessId")

            time_created = root.find(path_system + "/{*}TimeCreated")
            if time_created is not None:
                system_time = time_created.get("SystemTime")
                system_time = dateutil.parser.parse(system_time)
                system_time = system_time.astimezone(datetime.timezone.utc).replace(tzinfo = None)
                print(system_time)
            else: raise ValueError("Logs are wrong made")

            p = psutil.Process(int(pid))
            p_create_time = p.create_time()
            p_create_time = datetime.datetime.fromtimestamp(p_create_time, datetime.timezone.utc).replace(tzinfo=None)
            delta = (p_create_time - system_time).total_seconds()

            if abs(delta) > 5: # то есть если процесс был создан более чем через 5 секунд после записи, то это уже не тот процесс скорее всего
                print("Maybe PID is reused")
                raise ValueError("Process over")
            
            print(f"Process is launched with {name} and {pid}")
            # сетевые соединеpythния
            # kind='inet' -> IPv4, IPv6, TCP, UDP
            for c in p.net_connections(kind='inet'):
                src = f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "-"
                dst = f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "-"
                print(f"{src} -> {dst} {c.status}")
                # открытые файлы
            for f in p.open_files():
                print(f"{f.fd} {f.path}")
            for c in p.children(recursive=True):
                print(f"{c.pid}  {c.name()}  {c.status()}")
            filepath = p.exe()
            print(f'Путь до файла: {filepath}')
            print(f'Командная строка процесса: {" ".join(p.cmdline())}')
            print(f'Хэш бинаря: {sha256_file(filepath)}')
        except Exception as e:
            print(f"Ошибка обработки события: {e!r}")
        finally:
            event.Close()  # тоже PyEVT_HANDLE, тоже .Close()


if __name__ == "__main__":
    events = GetEventLogs(logtype, flags, query)
    ParseEvents(events)

