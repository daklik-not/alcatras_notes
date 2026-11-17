# /// script
# requires-python = ">=3.10"
# dependencies = ["pywin32"]
# ///
# platform: windows-only (pywin32 / winreg / WMI)

import win32evtlog
import xml.etree.ElementTree as ET

server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ | \
        win32evtlog.EVENTLOG_SEQUENTIAL_READ

xpath_query = "*[System[EventID=4663]]"

def DetectLocalStateAccess():
    query_handle = win32evtlog.EvtQuery(logtype, win32evtlog.EvtQueryChannelPath, xpath_query)
    
    while True:
        events = win32evtlog.EvtNext(query_handle, 10)
        if not events: 
            break
            
        for evt in events:
            xml_string = win32evtlog.EvtRender(evt, win32evtlog.EvtRenderEventXml)
            root = ET.fromstring(xml_string)

            obj_node = root.find(".//{*}Data[@Name='ObjectName']")
            proc_node = root.find(".//{*}Data[@Name='ProcessName']")
            pid_node = root.find(".//{*}Data[@Name='ProcessId']")
            time_node = root.find(".//{*}TimeCreated")

            #print(obj_node.text, proc_node.text, pid_node.text, time_node.text)
            if obj_node is not None and obj_node.text:
                process_name = proc_node.text if proc_node is not None else "Unknown"
                process_id = pid_node.text if pid_node is not None else "Unknown"
                time_created = time_node.get('SystemTime') if time_node is not None else "Unknown"
                print(f"{process_name} (PID {process_id}) accessed Local State at {time_created}")
if __name__ == "__main__":
    DetectLocalStateAccess()