import winreg

def checkValues(key, keyword):
    try:
        numValues = winreg.QueryInfoKey(key)[1]
    except OSError:
        return None
    for i in range(numValues):
        try:
            name, data, _vtype = winreg.EnumValue(key, i)
        except OSError:
            break
        if name.lower() == keyword.lower():
            return data
    return None

def checkLogonScripts():
    try:
        numUsers = winreg.QueryInfoKey(winreg.HKEY_USERS)[0]
    except OSError as e:
        print(f"cannot enumerate HKU: {e}")
        return

    for i in range(numUsers):
        try:
            userKey = winreg.EnumKey(winreg.HKEY_USERS, i)
        except OSError:
            continue

        regPath = f"{userKey}\\Environment"
        try:
            with winreg.OpenKey(winreg.HKEY_USERS, regPath, 0,
                                winreg.KEY_READ) as key:
                script = checkValues(key, "UserInitMprLogonScript")
        except FileNotFoundError:
            continue                      # у этого SID нет Environment
        except PermissionError:
            print(f"access denied: HKU\\{regPath}")
            continue
        except OSError as e:
            print(f"error HKU\\{regPath}: {e}")
            continue

        if script is not None:
            print(f"Logon script at HKU\\{regPath} : {script!r}")

checkLogonScripts()