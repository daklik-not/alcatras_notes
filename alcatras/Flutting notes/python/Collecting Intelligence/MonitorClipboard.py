
# /// script
# requires-python = ">=3.10"
# win32gui = ["win32.distutils.command"]
# dependencies = ["pywin32", "psutil"]
# ///

import win32gui, win32api, ctypes
from win32clipboard import GetClipboardOwner
from win32process import  GetWindowThreadProcessId
from psutil import Process
import win32clipboard

def print_clipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT).rstrip()
    print("Current Clipboard")
    print(data)
    win32clipboard.CloseClipboard()
    return 


allowlist = []
def processEvent(hwnd, msg, wparam, lparam):
    if msg == 0x031D:
        # WM_CLIPBOARDUPDAT - 0x031D
        try:
            win = GetClipboardOwner()
            # возвращает декскриптор окна, которое владееет буфером обмена
            # то есть откуда скопировали буквально
            pid = GetWindowThreadProcessId(win)[1]

           
          
            # функция которая по дескриптору окна win возвращает
            # (threadid, prorcess_id)
            p = Process(pid)
            name = p.name()
            if name not in allowlist:
                print(f"Clipboard modified by {name}")
                print_clipboard()
        except:
            print("Clipboard modified by unknown process")
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
def createWindow():
    wc = win32gui.WNDCLASS() # создаем обьект окна Windows
    wc.lpfnWndProc = processEvent # указываем обработчик событий окна
    wc.lpszClassName = 'clipboardListener' # уникальный внутри программы класс окна
    wc.hInstance = win32api.GetModuleHandle(None)
    # win32api.GetModuleHandle(None) - хэндл текущего исполняемого файла(None)
    # wc.hInstance - говорим что владелец окна мой процесс(чей хэндл мы передали типо)
    class_atom = win32gui.RegisterClass(wc)
    # RegisterClass - регистрацимя окна в системе
    # это 'атом' - 16битное целое число, которое Windows внутри себя
    # сопоставляет со строкой clipboardListener
    return win32gui.CreateWindow(class_atom, 'clipboardListener', 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
    """
Сигнатура win32gui.CreateWindow(
    className,    # [1] Имя класса окна или числовой class_atom из RegisterClass()
    windowName,   # [2] Заголовок окна (виден в диспетчере окон/отладчиках, на экране скрыт)
    style,        # [3] Стиль окна (0 = скрытое окно без рамки и флага WS_VISIBLE)
    x,            # [4] Позиция окна по оси X (для скрытого окна = 0)
    y,            # [5] Позиция окна по оси Y (для скрытого окна = 0)
    width,        # [6] Ширина окна в пикселях (для скрытого окна = 0)
    height,       # [7] Высота окна в пикселях (для скрытого окна = 0)
    parent,       # [8] Родительское окно: 0 — верхний уровень, win32con.HWND_MESSAGE (-3) — только для сообщений
    menu,         # [9] Дескриптор меню или ID дочернего элемента (0 — отсутствует)
    hinstance,    # [10] Дескриптор текущего процесса (win32api.GetModuleHandle(None))
    reserved      # [11] Дополнительные данные, передаваемые в событие WM_CREATE (обычно None)
) -> int (возвращает hwnd — уникальный дескриптор созданного окна)
"""

def setupListener():
    hwnd = createWindow()
    ctypes.windll.user32.AddClipboardFormatListener(hwnd)
    # короче это системный вызов, который говорит 
    # уведомлять hwnd окно об изменениях буфера обмена
    win32gui.PumpMessages()
    # у каждого GUI-потока есть своя очередь сообщений; 
    # окна этого потока получают сообщения через неё
    # с помощью PumpMessages, обработчик созданного окна блокируется
    # если нет сообщений
setupListener()