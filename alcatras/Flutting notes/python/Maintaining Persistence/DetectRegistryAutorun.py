import winreg 

hives = {
    "HKCU" : winreg.HKEY_CURRENT_USER,
    "HKLM" : winreg.HKEY_LOCAL_MACHINE 
}

paths = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"]

def checkRegAutorun(hive, path):
    autoruns = []
    try:
        with winreg.OpenKey(hive, path) as key:
            numValues = winreg.QueryInfoKey(key)[1]
            for i in range(numValues):
                    try:
                        # ивлекаем имя значения, данные, тип данных(но его пропускаем)
                        [name, data, _] = winreg.EnumValue(key, i)
                    except:
                        continue
                    if len(name) > 0:
                        autoruns.append([name, data])
                    return autoruns
# numValues - [ число подключей, число значений,  время когда создано было ]
# print(f"{hive}/{path} {numValues}")

    except Exception as e:
        return []

def printResults(hive, path, autoruns):
    print(f"Autoruns detected in {hive, path}")
    for autorun in autoruns:
        print(autorun[0], autorun[1],"\n")

def checkAutoruns():
    for hive in hives: # перебор ключей
        for path in paths:
            autoruns = checkRegAutorun(hives[hive], path)  
            if autoruns: # короче если непустой список вернется
                printResults(hive, path, autoruns)
    # HKU хива
    numKeys = winreg.QueryInfoKey(winreg.HKEY_USERS)[0] # количество подключей
    for i in range(numKeys):
        # просто строка с SUID по имени
        subKey = winreg.EnumKey(winreg.HKEY_USERS, i) 
        for path in paths:
            subpath = f"{subKey}\\{path}" # путь до RUN 
            autoruns = checkRegAutorun(winreg.HKEY_USERS, subpath)
            if autoruns:
                printResults("HKU", subpath, autoruns)
    
checkAutoruns()     