import win32evtlog 
import  xml.etree.ElementTree as ET
server = "127.0.0.1"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ | \
win32evtlog.EVENTLOG_SEQUENTIAL_READ

def QueryEventLog(eventID, filename = None):
    xpath_query = f"*[System[EventID={eventID}]]"
    query_handle = win32evtlog.EvtQuery(logtype, win32evtlog.EvtQueryChannelPath, xpath_query)
    while True:
        events = win32evtlog.EvtNext(query_handle, 10)
        if not events:
            break
        for evt in events:
            xml_string = win32evtlog.EvtRender(evt, win32evtlog.EvtRenderEventXml)
            root = ET.fromstring(xml_string)
            username = root.find(".//{*}Data[@Name='SubjectUserName']")
            domain = root.find(".//{*}Data[@Name='SubjectDomainName']")
            # Задание 1 - вывожу привилегии
            privileges_raw = root.find(".//{*}Data[@Name='PrivilegeList']")
            print(privileges_raw.text)
            print(username.text, domain.text)

QueryEventLog(4672)