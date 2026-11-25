import glob, os
from zipfile import ZipFile
from sys import platform
import tarfile
from pathlib import Path
# /// script
# requires-python = "==3.12"
# ///


archiveFiles = ["zip", "tar"]
emailFiles = ["pst", "ost"]

EXTRACT_DIR = Path.cwd() / "extracted_files"


def is_email_file(name):
    """Проверяет, что файл внутри архива - почтовый (pst/ost)."""
    return Path(name).suffix.lower() in {f".{ext}" for ext in emailFiles}


def unique_target(name):
    """Возвращает свободный путь в EXTRACT_DIR, чтобы не затирать уже извлечённые файлы."""
    target = EXTRACT_DIR / Path(name).name
    counter = 1
    while target.exists():
        target = EXTRACT_DIR / f"{Path(name).stem}_{counter}{Path(name).suffix}"
        counter += 1
    return target


def extract_archive(path, type):
    """Извлекает все pst/ost из архива (включая поддиректории) в EXTRACT_DIR."""
    extracted = []
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    match type:
        case "zip":
            with ZipFile(path, "r") as zf:
                for member in zf.namelist():
                    if is_email_file(member):
                        target = unique_target(member)
                        target.write_bytes(zf.read(member))
                        extracted.append(str(target))
        case "tar":
            with tarfile.open(path, "r:*") as tar:
                for member in tar.getmembers():
                    if member.isfile() and is_email_file(member.name):
                        f = tar.extractfile(member)
                        if f is not None:
                            target = unique_target(member.name)
                            target.write_bytes(f.read())
                            extracted.append(str(target))
    return extracted

def searchArchiveFile(filename, type):
    try:
        return extract_archive(filename, type)
    except:
        return list()

def findFiles():
    if platform == "win32":
        pattern = r"~\**\*." # win like пути
        # ~ домашняя директория
        # ** - все вложенные папки на всю глубину
        # \ разделитель папок
        # * любое имя файла
    else:
        pattern = r"~/**/*."
    in_pattern = pattern
    extensions = emailFiles + archiveFiles
    files = []
    for ext in extensions:
        pattern = in_pattern + ext
        pattern = os.path.expanduser(pattern) # убирает тильду
        f = glob.glob(pattern, recursive = True) 
        # эта штука нужна для поиска файлов и папок по маскам
        if ext in archiveFiles:
            for a in f:
                files.extend(searchArchiveFile(a, ext))
        else:
            files.extend(f)  
    print(files)
    return files

if __name__ == "__main__":
    findFiles()
   
