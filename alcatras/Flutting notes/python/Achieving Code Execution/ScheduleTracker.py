import os, pathlib, subprocess, csv, io, re, hashlib, psutil


def CheckValidTask(creator, task, taskname):
    allowlist = [r"Microsoft", "Mozilla", "Adobe Systems Incorporated"]
    extensions = [".exe", ".py", ".dll", ".bat", ".cmd", ".ps1", ".vbs", ".hta", ".msi", ".scr", ".js", ".jse", ".wsf", ".lnk"]
    trusted = [creator for x in allowlist if creator.startswith(x)]
    executable = [task for ext in extensions if ext in task]
    if executable:
        exe = parse_binary_path(task)
        p = os.path.expandvars(exe).lower()
        #print(p)
        if taskname.startswith("\\Microsoft\\"): # обцчный пользователь не может создавать там задачи
            return True
        if p.startswith("c:\\windows\\system32\\"):
            return True
        else:
            return trusted
    else:
        return True

def file_hash(task):
    exe = parse_binary_path(task)
    path = os.path.expandvars(exe).lower()
    try:
        with open(path, "rb") as f:
            return hashlib.file_digest(f, "sha256").hexdigest()
    except (OSError, ValueError) as e:
        return f"<error: {type(e).__name__}>"

def parse_binary_path(task):
    m = re.match(r'^"([^"]+)"', task) # re.match ищет только с начала строки
    '''
    ^ - начало строки
    ([^"])+ отрицание в группе захвата, типо захватывает все кроме "
    короче типо смотрим только первую "C:\....process.exe"
    ''' 
    if m: # если нашло что то, т:
        exe = m.group(1) # достать содержимое первой группы захвата
    else: # ^(.+?\.(?:exe|py|dll))
        m = re.match(r'^(.+?\.(?:exe|py|dll))(?=[\s,"]|$)', task, re.IGNORECASE)
    '''
    .+? - наименьшее возможное количество при котором остаток тоже совпадет
    ?: не создает группу
    (?=[\s,"]|$) - lookahead - просмотр вперед без захвата типо
    \s - пробел, то есть пробел, запятая, или кавычка или конец строки
    '''
    exe = m.group(1) if m else task.split(" ", 1)[0]
    return exe


def process_info_by_path(target_path):
    target = os.path.normcase(os.path.abspath(target_path))
    # тут медленно короче работает, но впадлу фиксить + нельзя 1 раз читать по факту
    for p in psutil.process_iter(["pid", "exe", "cmdline", "create_time", "username"]):
        try:
            exe = p.info["exe"] # типо доступ по ключу к обьекту process_iter
            if not exe:
                continue
            if os.path.normcase(exe) == target:
                return p
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue
    return None


raw = subprocess.check_output("schtasks /query /v /fo csv /nh", shell=True)
# fo = format output, /nh = no header
text = raw.decode("cp866", errors = "replace") # errors = replace - обработка битых байтов
results = list(csv.reader(io.StringIO(text)))
# io.StringIO - создает файлоподобный обьект в памяти, дает для csv.reader, который читает по строкам, удобный обьеки для итерации
# csv.reader() - разбивает на строки и поля

for res in results:
    result = [x.strip("\"") for x in res] # удаление кавыче по бокам типо
    if len(result) > 8:
        name = result[1]
        creator = result[7]
        task = result[8]
        status = result[3]
        #print(f'Creator:{creator}-Task:{task}')
        if not CheckValidTask(creator, task, name):
            proc = process_info_by_path(parse_binary_path(task))
            print(f'{name} {creator} {task} {status} {file_hash(task)}')
            if proc:
                print(f"Proc PID {proc.info["pid"]}, created={proc.info["create_time"]} user={proc.info["username"]}")
        