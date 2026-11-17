import re
from subprocess import check_output, CalledProcessError

def check_last_login(user: str) -> None:
    try:
        res = check_output(
            ["net", "user", user],
            text=True
        )
        m = re.search(r"(Last logon)\s*([^\r\n]+)", res)
        print(f"[{user}] Last logon: {m.group(1).strip()}")
    except Exception as e:
        pass
    
for user in ["tester", "Administrator", "0987a"]:
    check_last_login(user)