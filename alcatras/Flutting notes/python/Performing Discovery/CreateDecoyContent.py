import pathlib


def getTimeStamps(filename):
    fname = pathlib.Path(filename)
    stats = fname.stat()
    if not fname.exists():
        return []
    return (stats.st_birthtime, stats.st_mtime, stats.st_atime)

def createDecoyFiles(filenames):
    with open("decoys.txt", "w") as f:
        for file in filenames:
            (ctime, mtime, atime) = getTimeStamps(file)
            f.write(f"{file,ctime,mtime,atime}")

createDecoyFiles(decoys) 
decoys = [r"Documents\clients.csv",r"Documents\Resume.docx"]