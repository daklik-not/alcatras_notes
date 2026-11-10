import os, re, subprocess
from pathlib import Path
def findADS(d):
    for dirpath, dirnames, filenames, in Path.walk(d):
        for f in filenames:
            filename = dirpath / f
            cmd = f'Get-Item -Path "{filename}" -Stream *'
            cmd += "| Format-Table -Property \"Stream\" \
            -HideTableHeaders"
            results = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    cmd],  capture_output=True 
            )
            streams = results.stdout.decode("utf-8").split("\r\n")
            streams = [ s.strip() for s in streams ]
            streams = [ s for s in streams if len(s) > 1 ]
            if len(streams) > 1:
                print(f"ADS detected in {filename}")
                for s in streams:
                    print(f"\t {s}")
    
findADS(Path(r"C:\Users\daklik-not\Downloads"))

        