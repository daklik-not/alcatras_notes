import winreg,  os
from pathlib import Path

def readPathValue(reghive, regpath):
    with winreg.OpenKey(reghive, regpath, access = winreg.KEY_READ) as key:
        try:
    
            value, _ = winreg.QueryValueEx(key, "Path")
            return os.path.expandvars(value)
        except Exception as e:
            return None

def editPathValue(reghive, regpath, targetdir):
    stargetdir = str(targetdir)
    path = readPathValue(reghive, regpath) or ""
    # просто через нейронку нормализовал, уродливо, но в целом понятно
    if os.path.normcase(os.path.normpath(stargetdir)).rstrip("\\/") in {
        os.path.normcase(os.path.normpath(p)).rstrip("\\/")
        for p in os.path.expandvars(path).split(os.pathsep)
        if p.strip()
    }:
        return# то есть директория, которую мы хотим инжектить уже в path
    newpath = stargetdir + ";" + path # добавили ее в самое начало
    with winreg.OpenKey(reghive, regpath, access = winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, newpath)
        


reghive = winreg.HKEY_CURRENT_USER
regpath = "Environment"
targetdir = Path.cwd()
editPathValue(reghive, regpath, targetdir)