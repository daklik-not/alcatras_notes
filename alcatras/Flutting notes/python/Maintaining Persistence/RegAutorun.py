import shutil, winreg, subprocess
from pathlib import Path
# лучше полностью перейти на Path
filedir = Path.cwd() / "Temp"
if not filedir.is_dir(): filedir.mkdir() # создаем Temp если ее еще нет
filename = "benign.exe"
filepath = Path(filedir / filename) # путь до benign.exe итоговый 
 
if filepath.is_file():
    filepath.unlink()
# text = True -> типо декодирование из байт в строку
# вместо commandline, поставить реальный бинарник
p = subprocess.run(["python3", "BuildExe.py"] , capture_output = True, text = True)

''' BuildExe.py
PyInstaller.__main__.run([
    "RegAutorun.py",
    "--onefile",
    "--name", "benign",
    "--distpath", "Temp",
])
'''

if p.returncode != 0:
   print("Cannot Create Process")
   exit(0)

reghive = winreg.HKEY_CURRENT_USER
new_reghive = winreg.HKEY_USERS
regpath = r"Software\Microsoft\Windows\CurrentVersion\Run"


n = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
for i in range(n):
    suid = winreg.EnumKey(winreg.HKEY_USERS, i)
    new_regpath = str(suid) + "\\" + regpath
    try:
        with winreg.OpenKey(winreg.HKEY_USERS, new_regpath, 0, access=winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "SecurityScan", 0, winreg.REG_SZ, str(filepath))
            winreg.DeleteValue(key, "SecurityScan") # это что бы на реальной системе не засорять
    except Exception as e:
        print(e)

'''
try:
    with winreg.OpenKey(reghive, regpath, 0, access=winreg.KEY_WRITE) as key:
        winreg.SetValueEx(key, "SecurityScan", 0, winreg.REG_SZ, str(filepath))       
        print("Autorun added", filepath)
        # сразу удаляем
        winreg.DeleteValue(key, "SecurityScan")
        print("Autorun Deleted")
except Exception as e:
    print("Cant add to registry")
'''

