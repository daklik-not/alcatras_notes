import importlib.machinery
import sys
from pathlib import Path
from collections import defaultdict
import hashlib
import filecmp



def getImports():
    # все модули загруженные в память
    # модуль - 1 файл с исходным кодом
    # библиотека - целый набор, связанных модулей и пакетов
    before = list(sys.modules.keys())
    import test
    after = list(sys.modules.keys())
    new = [n for n in after if not n in before]
    return {name for name in new}

def getHash(file_path):
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.file_digest(f, "sha256")
            return file_hash.hexdigest()
    except Exception as e:
        print(e)
    return None

def checkFiles(path1, path2):
    hash1 = getHash(path1)
    hash2 = getHash(path2)
    # короче для None сравнений лучше использовать is, потому что
    # == может быть переопределен
    if hash1 is None: print(f"Cannot calculate the hash of {path1}")
    if hash2 is None: print(f"Cannot calculate hash of {path2}")
    if not (hash1 and hash2):
        return None
    if hash1 != hash2:
        print("Hash difference in ")
        print(f"\t{path1}:{hash1}")
        print(f"\t{path2}:{hash2}")
        return False
    return True

def fast_check_dirs(dcmp, path, cond):
    obj = dcmp.right_only if cond == "right" else dcmp.left_only
    found = False
    for cdir in obj:
        p = path / cdir
        if p.is_dir():
            print(f"Directory {p} only in {path}")
        else:
            print(f"File {p} only in {path}")
        found = True
    return found

def checkDirs(path1, path2):
    same = True
    dcmp = filecmp.dircmp(path1, path2, ignore = None, hide = None)
    for cfile in dcmp.common_files:
        fpath1 = path1 / cfile
        fpath2 = path2 / cfile
        file_result = checkFiles(fpath1, fpath2)
        if file_result != None:
            same =  same and file_result
        else: same = False
    if fast_check_dirs(dcmp, path1, "left"): same = False
    if fast_check_dirs(dcmp, path2, "right"): same = False
    for name in dcmp.common_funny:
        left, right  = path1 / name,  path2 / name
        print(f"Different type {left} vs {right}")
        same = False
    for cdir in dcmp.common_dirs:
        same = checkDirs(path1 / cdir, path2 / cdir) and same
    return same

def checkAll(path1, path2):
    path1 = Path(path1)
    path2 = Path(path2)
    if path1.is_file() and path2.is_file():
        return checkFiles(path1, path2)
    elif path1.is_dir() and path2.is_dir():
        return checkDirs(path1, path2)
    else:
        print("Cannot compare file and directory")
        return 0

def loaded_origin(name):
    mod = sys.modules[name]
    # getattr получение атрибута от обьекта
    # нужно тогда когда имя атрибута неизвестно на момент написания кода 
    pkg_paths = list(getattr(mod, "__path__", None) or [])
    if pkg_paths:
        return Path(pkg_paths[0]).resolve() # типо вернули разрезолвенную директорию
    spec = getattr(mod, "__spec__", None)
    origin = getattr(spec, "origin", None) # достаю обьект spec и из него origin
    if origin in (None, "built-in", "frozen", "namespace"):
        return None
    file = getattr(mod, "__file__", None) or origin
    return Path(file).resolve()

def compareModules(modules):
    for module, path_list in modules.items():
        ref = loaded_origin(module)
        if ref is None:
            continue
        for path in path_list:
            if path == ref:
                continue
            print(f"Duplicate {module}:\n\t{ref}\n\t{path}")
            if checkAll(ref, path):
                print("Modules/packages are identical")

def addFile(path, levels, index):
    suffixes = importlib.machinery.all_suffixes()
    root = Path(path)
    if not root.is_dir(): return None
    for child in root.iterdir():
        if child.is_dir() and index == len(levels) - 1: # пакет
            if (root / levels[index] / "__init__.py").is_file(): # проверка на наличие __init__.py
                return (root / levels[index]).resolve() # вернули нужную пакетную диру
        if child.is_file() and index == len(levels) - 1 : # модуль
            fname = child.name
            if fname.startswith(levels[index]) and fname[len(levels[index]):] in suffixes:
                return child.resolve() # то есть мы нашли файл и сразу добавили его
        if child.is_dir(): # просто дира на пути
            dname = child.name
            if dname == levels[index]: # нашли диреткторию, надо спуститься 
                new_path = root / dname
                return addFile(new_path, levels, index + 1)

def findModules(imports):
    mods = defaultdict(list)
    for p in sys.path:
        for name in imports:
            levels = name.split(".")
            found = addFile(p, levels, 0)
            if found is not None:
                mods[name].append(found)
    return mods

imports = getImports()

modules = findModules(imports)


compareModules(modules)
