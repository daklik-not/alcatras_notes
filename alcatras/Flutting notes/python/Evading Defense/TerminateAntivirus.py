# /// script
# requires-python = ">=3.10"
# dependencies = ["psutil"]
# ///

import psutil, os, signal

av_list = ["notepad"]

for process in psutil.process_iter():
    for name in av_list:
        if name in process.name().lower():
            os.kill(process.pid, signal.SIGTERM)
