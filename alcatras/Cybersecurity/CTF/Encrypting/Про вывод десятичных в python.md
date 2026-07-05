Чтобы вывести число в десятичке нужно иcпользовать Decimal
Пример:
```
from decimal import Decimal, getcontext
getcontext().prec = 100  
ct = Decimal(str(ct))
e = Decimal(str(e))
m = ct ** (Decimal('1') / e)
print(f"Результат: {m}")
print(int(m).to_bytes(100,"big"))
```
