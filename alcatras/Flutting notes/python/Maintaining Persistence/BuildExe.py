# BuildExe.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    "RegAutorun.py",
    "--onefile",
    "--name", "benign",
    "--distpath", "temp"
])