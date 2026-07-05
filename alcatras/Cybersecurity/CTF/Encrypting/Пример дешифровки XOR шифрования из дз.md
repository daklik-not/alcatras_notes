```
s = "MTUwNi06LjkpNSByOBo6JB5nNhE8cSIaIisoOCIRJXIJK31hJQkjfmMtCS16JjIr"
import base64
deb64 = base64.b64decode(s)
from itertools import *
for akey in product("ABCDEFGHIJKLMNOPQRTUVWXYZ", repeat = 5):
    key = ''
    for i in akey: key += i
    keyar = [ord(i) for i in key]
    s1 = ''
    for i in range(0, len(deb64)):
        s1+= chr(deb64[i]^(keyar[i%len(key)]))
    passwords = ["ctfschool"]
    for i in passwords:
        if i in s1 and (not(""in s1)):
            print(s1)
            print()
            break
```