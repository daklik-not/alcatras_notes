```
from coffee import  keystream, SEED
with open('secret.enc', 'rb') as file:
    file_data = file.read()
key_bytes = keystream(SEED, len(file_data))
flag = bytearray()
for i in range(len(key_bytes)):
	flag.append(key_bytes[i]^file_data[i])
flag = bytes(flag)
for i in flag: print(chr(i), end='')
```