# pip install PyMI
# PyMI работает как drop-in замена для wmi, используя MI API
import wmi  # после установки PyMI этот импорт будет использовать MI
import subprocess

c = wmi.WMI()

# Получаем список администраторов (современный API MI)
admins = set()

'''
Win32_Group - динамическое свойство
появляется только при вызове __getattr__

def __getattr__(self, name):
    return f"Я создал атрибут '{name}' на лету!"

короче это надо чтобы не писать одинаковый код для 
кучи разных классов
'''

for group in c.Win32_Group(Name="Administrators"):
    # короче associators это метод который позволяет находиться связи
    # между обьектами из разных классов
    # wmi_result_class - с каким классом связываем
    for user in group.associators(wmi_result_class="Win32_UserAccount"):
        admins.add(user.Name)

for user in c.Win32_UserAccount():
    print(f"Username: {user.Name}")
    print(f"Administrator: {user.Name in admins}")
    print(f"Disabled: {user.Disabled}")
    print(f"Domain: {user.Domain}")
    print(f"Local: {user.LocalAccount}")
    print(f"Password Changeable: {user.PasswordChangeable}")
    print(f"Password Expires: {user.PasswordExpires}")
    print(f"Password Required: {user.PasswordRequired}")
    print()

print("Password Policy:")
result = subprocess.run(["net", "accounts"], capture_output=True, text=True, check=True)
print(result.stdout)

'''
Современным методом считается получение данных через Get-Ciminstance
имена классов вроде те же там
'''