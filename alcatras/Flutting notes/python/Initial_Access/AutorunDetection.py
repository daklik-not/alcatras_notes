import win32con
from win32api import GetLogicalDriveStrings
from win32file import GetDriveType
import os.path
import psutil
import datetime


def GetRemovableDrivers():
    drive_strings =  GetLogicalDriveStrings()          # "C:\\\0D:\\\0E:\\\0\0"
    drives = [d for d in drive_strings.split("\x00") if d]     # ['C:\\', 'D:\\', 'E:\\']
    return [d for d in drives if GetDriveType(d) == win32con.DRIVE_REMOVABLE]


def CheckAutorun(drive):
    filename = drive + "Autorun.inf"
    if os.path.isfile(filename):
        print(f"Autorun file at {filename}")
        with open (filename, "r") as f:
            for line in f:
                if line.lower().startswith("Open"):
                    ind = line.index("=")
                    return line[ind + 1:].rstrip()
    else:
        return None

def DetectAutorunProcess(executable):
    for proc in psutil.process_iter(): # итерация по всем процессам системы
        if executable == proc.name():
            print(f"Autorun file running with PID {proc.pid}")
            print(f"Autorun file running with PPID {proc.ppid()}")
            created = datetime.datetime.fromtimestamp(proc.create_time())
            print(f"Process Creation time: {created:%Y-%m-%d %H:%M:%S}")
for drive in GetRemovableDrivers():
    executable = CheckAutorun(drive)
    if executable:
        DetectAutorunProcess(executable)
