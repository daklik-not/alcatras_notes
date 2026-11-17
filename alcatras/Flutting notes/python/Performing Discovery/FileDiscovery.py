import re
import docx2txt
import chardet
import pypdf
from pathlib import Path
from python_calamine import CalamineWorkbook
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 МБ

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b')
SSN_REGEX = re.compile(r'\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b')
IP_REGEX = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
PHONE_REGEX = re.compile(r'\+[1-9][0-9]{6,14}\b')


'''
?:  -  незахватывающая группа, то есть мы не создаем группу в скобках
'''


def is_binary(file_path): # проверка является ли файл бинарным
  with open(file_path, 'rb') as f:
    chunk = f.read(1024) 
    return b'\x00' in chunk
  
def detectEncoding(filepath):
    with open(filepath, "rb") as f:
        raw_data = f.read(64 * 1024)
        result = chardet.detect(raw_data)
        return result['encoding'] or "utf-8"
        
def findPII(data):
    matches = set(EMAIL_REGEX.findall(data))
    matches |= set(PHONE_REGEX.findall(data))
    matches |= set(IP_REGEX.findall(data))
    matches |= set(SSN_REGEX.findall(data))
    return matches

def printMatches(matches):
    for match in matches:
        print(f"{match}")

def parseDocx(root, docs):
    for doc in docs:
        if doc.startswith("~$"):
            continue 
        filedir = root / doc
        try:
            if filedir.stat().st_size > MAX_FILE_SIZE:
                continue
        except OSError:
            continue
        try:
            data = docx2txt.process(str(filedir)) 
            matches = findPII(data)
            if matches: printMatches(matches)       
        except Exception as e:
            pass

def parseText(root, txts):
    for txt in txts:
        filedir = root / txt
        try: # скипаем болшие файлы
            if filedir.stat().st_size > MAX_FILE_SIZE:
                continue
        except OSError:
            continue
        try:
            encoding = detectEncoding(filedir)
            with open(filedir, "r", encoding=f'{encoding}', errors='ignore') as f:
                data = f.read()
            matches = findPII(data)
            if matches:
                printMatches(matches)
        except Exception as e:
            pass

def parsePDF(root, txts):
    for pdf in txts:
        file_path = (root / pdf).resolve()
        full_text = ""
        try:
            reader = pypdf.PdfReader(str(file_path))
            for page in reader.pages:
                text = page.extract_text() or ""
                full_text += text + "\n"

            matches = set(findPII(full_text))
            if matches:
                printMatches(matches)
        except Exception:
            print("Cannot open PDF file")
    
def parseXLSX(root, txts):
    for pdf in txts:
        file_path = (root / pdf).resolve()
        try:
            wb = CalamineWorkbook.from_path(file_path)
            parts = []
            full_text = ""
            for sheet_name in wb.sheet_names: # итерируем по листам
                rows = wb.get_sheet_by_name(sheet_name).to_python() # получаем листы и делаем список списков
                for row in rows:
                    for cell in row: full_text += (str(cell) + " ") 
            matches = findPII(full_text)
            if matches: printMatches(matches)
        except OSError:
            print("Cannon open XLSX file")


def findFiles(directory):
    for root, dirs, files in Path.walk(directory): # root это обьект Path
        f_docx, f_pdf, f_txt, f_xlsx, f_json = ([] for _ in range(5))

        for f in files:
            if f.endswith(".docx"): f_docx.append(f)
            if f.endswith(".pdf"): f_pdf.append(f)
            if f.endswith(".xlsx"): f_xlsx.append(f)
            if not is_binary(Path(root / f)):
                f_txt.append(f)

        parseDocx(root, f_docx)
        parseText(root, f_txt)
        parsePDF(root, f_pdf)
        parseXLSX(root, f_xlsx)

download_dir = Path.home() / "Downloads"
print(f"Сканирую папку: {download_dir}...\n")
findFiles(download_dir)
print("\nСканирование завершено.")