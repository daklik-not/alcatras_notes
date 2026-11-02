import sys
from pathlib import Path
from collections import defaultdict

def getImports():
    # все модули загруженные в память
    # модуль - 1 файл с исходным кодом
    # библиотека - целый набор, связанных модулей и пакетов
    before = list(sys.modules.keys())
    import test
    after = list(sys.modules.keys())
    new = [n for n in after if not n in before]
    return {name.split(".")[0] for name in new}


def findModules(imports):
    mods = defaultdict(list)
    path = sys.path # все директории, где python ищет модули/библиотеки
    path[0] = Path.cwd()
    for p in path:
        '''
        Короче эта штука позволяет спускаться вниз 
        r - путь до текущей диеректории
        d - все поддиректории
        f - все файлы
        он рекурсивно спускается вниз по дереву поддиректорий \
        от указанного пути
        '''
        for r, d, f in Path(p).walk():
            for i in imports:
                # случай когда библиотека это единичный файл
                files = [file for file in f if file.startswith(i + ".py")]
                for file in files:
                    filepath = r / file
                    mods[i].append(filepath)
                # случай когда либа, это набор файлов - смотрим папку
                filepath = r / i / "__init__.py"
                if i in d and filepath.is_file():
                    mods[i].append(filepath)
    return mods

imports = getImports() # типо получили модули, которые загружены в память и которых раньше не было
modules = findModules(imports) # теперь пытаемся найти где они лежат
for m in modules:
    if len(modules[m]) > 1:
        print(f"Duplicate verisions of {m} found")
        for x in set(modules[m]):
            print(f"\t{x}")
