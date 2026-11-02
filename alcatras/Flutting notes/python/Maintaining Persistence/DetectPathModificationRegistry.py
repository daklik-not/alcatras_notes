import winreg
from datetime import datetime, timedelta, timezone

delta = timedelta(weeks = 2) 
t = (datetime.now(timezone.utc) - delta) # timestmap который был 2 недели назад просто

def ft_to_dt(ft):
    return datetime(1601, 1, 1, tzinfo = timezone.utc) + timedelta(microseconds = ft // 10)


def checkTimeDelta(time):
    return (t < ft_to_dt(time)) #получается что недавнее тогда

def checkPath(hive, hivename, regpath):
    try:
        with winreg.OpenKey(hive, regpath, access = winreg.KEY_READ) as key:
            result = winreg.QueryInfoKey(key)
            # 0 число подключей, 1 когда последний раз редачили 2 это 10^-7
            if checkTimeDelta(result[2]):
                print(f"Path {hivename}\\{regpath} has potentially bene modified")
                print("Current Path: ")
                val = winreg.QueryValueEx(key, "Path")[0]
          #      print("here2")
                for v in val.split(";"):
                    print(f"\t{v}")
    except Exception as e:
        print(e, ": checkPath")
        return
    
def checkPaths():
    checkPath(winreg.HKEY_LOCAL_MACHINE, "HKLM", r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    # типо посмотрели системные пути как я пон
    checkPath(winreg.HKEY_CURRENT_USER, "HKCU", "Environment")
    # типо посмотрели для текущего пользователя 
    try:
        numUsers = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
        for i in range(numUsers):
            userKey = winreg.EnumKey(winreg.HKEY_USERS, i) # извлекаем i пользователя
            regPath = f"{userKey}\\Environment"
            checkPath(winreg.HKEY_USERS, "HKU", regPath)
    except Exception as e:
        print(e, ": checkPaths")
        return 

checkPaths()
