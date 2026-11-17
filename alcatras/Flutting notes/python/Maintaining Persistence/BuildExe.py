# /// script
# requires-python = ">=3.10"
# dependencies = ["pyinstaller"]
# ///

# BuildExe.py
import PyInstaller.__main__

PyInstaller.__main__.run([
    "RegAutorun.py",
    "--onefile",
    "--name", "benign",
    "--distpath", "temp"
])