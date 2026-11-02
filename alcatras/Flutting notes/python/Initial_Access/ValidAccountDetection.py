import win32evtlog
from collections import defaultdict
server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ | \
        win32evtlog.EVENTLOG_SEQUENTIAL_READ
import pandas as pd

# EVENTLOG_FORWARDS_READ  - от начала к концу журнала
# EVENTLOG_SEQUENTIAL_READ - читает события последовательно

def QueryEventLog(eventID):
        logs = []
        #h = win32evtlog.OpenEventLog(server, logtype) # живой лог
        h = win32evtlog.OpenBackupEventLog(None, "Practice-Security.evtx") # сохраненный лог
 
        # типо аналог open() - возвращает дескриптор журнала
        try:
                while True: # ReadEventLog отдает только порцию
                        events = win32evtlog.ReadEventLog(h, flags, 0)
                        if events:
                                for event in events:
                                        if event.EventID == eventID:
                                                logs.append(event)
                        else:
                                break
        finally:
                win32evtlog.CloseEventLog(h)
        return logs

def DetectBruteForce():
        account_inf = defaultdict(list)
        events = QueryEventLog(4625) # неудачная авторизация
        for event in events:
                time = event.TimeGenerated
                account = event.StringInserts[5] # StringInserts это значения в EventData в том же порядке что и в логах
                if not account or account.endswith("$"):
                        continue
                account_inf[account].append(time)
        # Sigma Rule
        for account, times in account_inf.items():
                times = sorted(times)
                s = pd.Series(1, index=pd.DatetimeIndex(times))
                counts = s.rolling('5min').count()
                if max(counts) >= 3:
                        print(f"User {account} was bruteforced")

def CheckDefaultAccounts():
        with open("defaults.txt", "r") as f:
                defaults = [line.split(maxsplit=1)[0] for line in f if line.strip()]
        with open("allowlist.txt", "r") as f:
                allowed = f.read().splitlines()
        events = QueryEventLog(4624)
        for event in events:
                if event.StringInserts[8] in ("2", "3", "10"):     # LogonType: Network / RemoteInteractive
                        if event.StringInserts[5] in defaults:      # TargetUserName
                                if event.StringInserts[18] not in allowed:  # IpAddress
                                        print(f"Unathorized login to {event.StringInserts[5]} from {event.StringInserts[18]}")

                                        
DetectBruteForce()
CheckDefaultAccounts()
