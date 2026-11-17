import pathlib

def getTimeStamps(filename):
    fname = pathlib.Path(filename) 
    stats = fname.stat() # короче тут вся системная информация о файле
    if not fname.exists(): return []
    return (stats.st_birthtime, stats.st_mtime, stats.st_atime)

def checkTimeStamps(filename, create, modify, access):
    stats = getTimeStamps(filename)
    if len(stats) == 0:
        return False # File deleted
    (ctime,mtime,atime) = stats
    if float(create) != float(ctime):
        return False    # File creation time is incorrect
    elif float(modify) != float(mtime):
        return False    # File modify time is incorrect
    elif float(access) != float(atime):
        return False    # File access time is incorrect
    return True

def checkDecoyFiles():
    with open("decoys.txt", "r") as f: # это типо файл с настройками для файла
        for line in f:
            vals = line.rstrip().split(",")
            if not checkTimeStamps(vals[0], vals[1], vals[2], vals[3]):
                print(f"{vals[0]} was modified")


checkDecoyFiles()