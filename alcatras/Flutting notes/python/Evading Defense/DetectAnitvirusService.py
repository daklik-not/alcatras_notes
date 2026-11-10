import winreg, psutil, subprocess
from psutil import NoSuchService

av_list = ["WinDefend"]
reghive = winreg.HKEY_LOCAL_MACHINE
regpath = r"SYSTEM\CurrentControlSet\Services"

def checkAV_run(service_name):
    try:
        svc = psutil.win_service_get(service_name)
        if svc.status() != "running":
            subprocess.run(["sc", "start", service_name], check = True)
    except NoSuchService:
        print(f"{service_name} Service is not installed")

try:
    with winreg.OpenKey(reghive, regpath, 0, access=winreg.KEY_READ) as key:
        numKeys = winreg.QueryInfoKey(key)[0]
        for i in range(numKeys):
            subkey = winreg.EnumKey(key, i)
            if not any(name in subkey for name in av_list):
                continue
            try:
                with winreg.OpenKey(reghive, f"{regpath}\\{subkey}", 0, winreg.KEY_ALL_ACCESS) as k:
                    val, _ = winreg.QueryValueEx(k, "Start")
                    if int(val) == 4:
                        print(f"Service {subkey} is NOT set to run automatically")
                        winreg.SetValueEx(k, "Start", 0, winreg.REG_DWORD, 2) # установили в 4 сразу
                    checkAV_run(subkey)
            except (FileNotFoundError, OSError):
                pass
except OSError as e:
    print(e)
