import os, sqlite3, time
from datetime import datetime, timedelta

user = ""
profile = ""
firefoxPath = r"C:\Users\0987a\AppData\Roaming\Mozilla\Firefox\Profiles\ow7ajeo5.default-release\cookies.sqlite"


def createFakeCookie(name, value, host, path):
    now = datetime.now()

    expiry = int((now + timedelta(weeks=4)).timestamp())
    now_us = time.time_ns() // 1000 # time_ns - время в наносекундах
    lastAccessed = now_us
    creationTime = now_us
    query = f"""INSERT INTO moz_cookies
(`name`,`value`,`host`,`path`,`expiry`,`lastAccessed`,`creationTime`,`isSecure`,`isHttpOnly`,`schemeMap`)
VALUES ('{name}','{value}','{host}','{path}',{expiry},{lastAccessed},{creationTime},0,0,2);"""
    conn = sqlite3.connect(firefoxPath)
    c = conn.cursor()
    c.execute(query) # здесь другие не видят изменения
    conn.commit() # здесь уже видят
    c.close()
    return 

createFakeCookie("ASDF","name",".fake.com","/") 