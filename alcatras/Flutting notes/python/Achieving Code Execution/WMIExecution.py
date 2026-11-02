import subprocess, wmi

def WMIProcessCreation(name):
    c = wmi.WMI() # обьект WMI
    processID, returnValue = c.Win32_Process.Create(CommandLine=name)
    print(f'Process {name} created with PID:{processID}')

def PSProcessCreation(name):
    command = ["powershell", 
               "& { invoke-wmimethod win32_process -name create -argumentList notepad.exe | select ProcessId | % { $_.ProcessId} | Write-Host}"
               ]
    # shell = True -> передает строкой в системный shell(cmd), иначе Python сам создает процесс
    # capture_output = True, отлавливаем ввод в stdout процесса
    p = subprocess.run(command, shell=True, capture_output = True)
    if p.returncode == 0:
        print (f"Process {name} created with Powershell, PID is {p.stdout.decode("utf-8")}")

command = "notepad.exe"
WMIProcessCreation(command)
PSProcessCreation(command)