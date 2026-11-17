# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "aioftp",
#     "telnetlib3",
# ]
# ///

import ftplib
from time import sleep
import telnetlib3 # устарвевшая
import asyncio, aioftp



async def FTPConnection(ip, username, password):
    try:
        async with aioftp.Client.context(ip,  21, username, password) as client:
            pwd = await client.get_current_directory()
            print(pwd)
    # короче отлавливаем ошибку авторизации
    except aioftp.errors.StatusCodeError as e:
        if '530' in e.received_codes:
            print("FTP: Invalid Credentials")
    
# async def превращает обычную функцию в корутину
# корутина это функция которую можно постававить на паузу и возобновить
# await - ждем данные, типо отсюда коллбек
# await можно писать только в корутинах
async def read_until_prompt(reader, timeout=3, chunk_size=1024):
    """
    Читает данные из reader, пока не получит EOF или таймаут.
    Возвращает накопленный буфер.
    """
    buffer = ""
    while True:
        try:
            chunk = await asyncio.wait_for(reader.read(chunk_size), timeout=timeout)
            if not chunk:
                break  # Соединение закрыто сервером
            buffer += chunk
        except asyncio.TimeoutError:
            print("[*] Reading timeout")
            break
    return buffer


async def TelnetConnection(ip, username, password):
    # Правильно: сначала await, потом распаковка
    reader, writer = await telnetlib3.open_connection(ip, 23)
    
    try:
        await reader.readuntil(b"login: ") # типо ждем пока не прочитаетася
        writer.write(username + "\n")
        await writer.drain()
        
        await reader.readuntil(b"Password: ")
        writer.write(password + "\n")
        await writer.drain()
        
        # ожидание с ограничением по времени
        buffer = await read_until_prompt(reader)
        session = ""
        await writer.drain()
        if "Login incorrect" in buffer:
            print("Invalid credentials")
        elif "$" in buffer:
            print("Remote shell started")
            commands = ["ss", "ifconfig", "whoami"]
            for c in commands: 
                writer.write(c + "\n\n")
                c_res = await read_until_prompt(reader)
                print(c_res)
            writer.write("exit\n")
        return 
    finally:
        # Гарантируем закрытие соединения
        writer.close()
        await writer.wait_closed()

ip  = "127.0.0.1"
username = "daklik-not"
password = "Kaori~2015"
asyncio.run(TelnetConnection(ip, username, password))
asyncio.run(FTPConnection(ip, username, password))