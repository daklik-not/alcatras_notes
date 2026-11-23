# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "psutil",
# ]
# ///

import psutil, subprocess

'''
Вывод всех атрибутов которые можно использовать 
p = psutil.Process()
available_attrs = list(p.as_dict().keys())
print(available_attrs)
'''

def find_net_shares():
    
    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-SmbMapping | Select-Object -ExpandProperty LocalPath",
        ],
        capture_output=True,
        text=True,
    )
    drives = result.stdout.strip().splitlines()
    return drives

drives = find_net_shares()

for proc in psutil.process_iter(['exe','pid', 'environ']):
    exe_path = proc.info['exe']
    if str(exe_path).startswith("\\\\"):
        print(f"Running process in network folder: {exe_path}")
        continue
    for drive in drives:
        if str(exe_path).startswith(drive):
            print(f"Running process in shared folder: {exe_path}")