import win32evtlog
import xml.etree.ElementTree as ET

server = "localhost"
logtype = "Security"

def _open_query(logtype = None, filename = None, eventID = 4657):
    query = f"*[System[(EventID={eventID})]]" # получается сразу берем нужный EventID
    # то есть типо если filename, то идем по названию
    if filename:
        flags = win32evtlog.EvtQueryFilePath # 
        path = filename
    # а если нет, то использует тип лога
    else:
        flags = win32evtlog.EvtQueryChannelPath
        path = logtype
    return win32evtlog.EvtQuery(path, flags, query , None)

def _collect_events(query_handle, batch_size = 64):
    handles = []
    while True:
        try:
            events = win32evtlog.EvtNext(query_handle, batch_size)
        except win32evtlog.error as e:
            if e.winerror == 259: # то есть дочитали до конца
                break 
            raise
        if not events:
            break
        handles.extend(events)
    return handles # короче собрали все хэндлы

def _render_event(handle, WANTED_DATA):

    xml_str = win32evtlog.EvtRender(handle, win32evtlog.EvtRenderEventXml)
    # типо отрендерили в XML строку
    root = ET.fromstring(xml_str)
    # типо обьект xml
    event = {} # cловарь который содержит само событие

    for node in root.findall(".//{*}EventData/{*}Data"):
        name = node.get("Name")
        if name in WANTED_DATA:
            event[name] = node.text
    return event

def QueryEventLog(eventID, WANTED_DATA, filename = None):
    logs = []
    query_handle = _open_query(logtype = logtype, filename = filename, eventID = eventID)
    try:
        raw_events = _collect_events(query_handle) # короче это куча хэндлов
        for handle in raw_events:
            try:
                logs.append(_render_event(handle, WANTED_DATA))
            finally:
                handle.close()
    finally:
        query_handle.close()
    return logs
       # query_handle.close()

def detectPathModification():
    WANTED_DATA = ("ObjectName", "ObjectValueName", "OldValue", "NewValue",
                   "ProcessName", "ProcessId")
    events = QueryEventLog(4657, WANTED_DATA)
    for event in events:
        if event.get("ObjectValueName") != "Path":
            continue
        key = event.get("ObjectName") or ""
        oldPath = (event.get("OldValue") or "").split(";")
        newPath = (event["NewValue"] or "").split(";")
        additions = [d for d in newPath if d not in oldPath]
        deletions = [d for d in oldPath if d not in newPath]
        process = event["ProcessName"] or "?"
        pid = event["ProcessId"] or "?"
        print(f"Path at {key} is modified by {process} {pid}")
        if additions:
            print("\tAdditions:")
            for a in additions:
                print(f"\t\t{a}")
            if deletions:
                print("\tDeletions:")
                for a in deletions:
                    print(f"\t\t{a}")
        if sorted(oldPath) == sorted(newPath) and oldPath != newPath:
            print("Ist reordered")
            
detectPathModification()                       
   

