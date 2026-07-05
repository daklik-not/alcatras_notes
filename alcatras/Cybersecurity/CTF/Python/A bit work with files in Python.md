
Итератор - штука, которая позволяет независимо от структуры данных выводит значения элементов. Условно вот этот код будет работать для всех контейнеров (с похожей структурой очевидно).
```c
// для списка, вектора, массива, сета и своих похожих структур
auto it = a.begin(); 
for (int i = 0 ; i < a.size(); ++i) {
	std::cout << *it << std::endl; it++;
}
//для хэш таблицы
    auto it = a.begin();
    for (int i = 0 ; i < a.size(); ++i) {
        std::cout << it->first << " " << it->second << std::endl;
        it++;
    }

```

#### Работа с файлами через Path.
```c
from pathlib import Path

basepath = Path('my_directory/')
files_in_basepath = basepath.iterdir() //это итератор
for item in files_in_basepath:
    if item.is_file(): // является файлом? 
        print(item.name)
// если директория то примерно так  isdir() 
```

```c
for path in current_dir.iterdir():
...     info = path.stat() // обьект info содержит информацию для файла
...     print(info.st_mtime) //st_mtime - последнее время редактирования [сек]
```
#### Cоздание директорий
![[Pasted image 20260117153820.png]]
Под multiple подразумеваются деревья каталогов типо
Типо так
```c
import pathlib

p = pathlib.Path('2018/10/05')
p.mkdir(parents=True, exist_ok = True)
//parent=True - создает все родительские директории
//exist_ok = True - если директория существует не вызывает ошибку
```
#### Filename pattern
```c
//python strings
 fname.endswith('.txt'):
 fname.startswith()
 //через fnmatch
if fnmatch.fnmatch(filename, '*.txt');
* любой количество символов, ? один символ.
//glob
list = glob.glob(pattern) //все файлы по шаблону в текущей директории
for file in glob.iglob('**/*.py', recursive=True): 
// буквально find, возвращает итератор отлично от glob
for name in p.glob('*.p*'): // использование с Path
...     print(name)
```
#### Traversing directories
```c
for dirpath, dirnames, files in os.walk('.', topdown=False):
    print(f'Found directory: {dirpath}')
    for file_name in files:
        print(file_name)
        
//`topdown=False` сначала выводим файлы в поддиректориях
```
#### Temporary files/directories
Все написано в скопированных комментах
```c
from tempfile import TemporaryFile

# Create a temporary file and write some data to it
fp = TemporaryFile('w+t')
fp.write('Hello universe!')

# Go back to the beginning and read data from file
fp.seek(0)
data = fp.read()

# Close the file, after which it will be removed
fp.close()
```

```c
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
print('Created temporary directory ', tmpdir)
  os.path.exists(tmpdir)
```

#### Deleting Files and Directories
```c
os.remove(path) // удаляет файл, но не директорию(ошибка)
os.rmdir(path) // удаляет ПУСТУЮ директорию
//Чтобы удалить непустую директорию -
shutil.rmtree(trash_dir) // удалит все дерево 
```

#### Managing Files
Копирование файлов
```c
import shutil

src = 'path/to/file.txt'
dst = 'path/to/dest_dir'
shutil.copy(src, dst)
//работает точно как cp, если dst - файл, то он перезапишет файл, метаданные не копируются
shutil.copy2(src, dst) //+metadata
```
Копирование директорий
```c
import shutil
shutil.copytree('data_1', 'data1_backup') 
//скопирует все дерево директорий от текущей папки
```
Переместить файлы
```c
import shutil
shutil.move('dir_1/', 'backup/')
// если есть поместит в backup, если нет просто переименуется
```
Переименование
```c
os.rename(fname, sname)
```

#### Archiving - Только ZIP
Создание Zip обьекта
```c
import zipfile
with zipfile.ZipFile('data.zip', 'r') as zipobj:
	zipobj.namelist() // список файлов
	bar_info = zipobj.getinfo('sub_dir/bar.py') // информация
	bar_info.file_size // размер оригинальный
	bar_info.date_time // последнее редактирование\
	bar_info.compress_size // сжатый размер
```
Разархивирование
```c
data_zip.extract('file1.py') // 1 файл
data_zip.extractall(path='extract_dir/')  // все в другую
pwd_zip.extractall(path='extract_dir', pwd='Quish3@o') // архив с паролем
```
Создание
```c
import zipfile
// для нового архива
file_list = ['file1.py', 'sub_dir/', 'sub_dir/bar.py', 'sub_dir/foo.py']
with zipfile.ZipFile('new.zip', 'w') as new_zip:
    for name in file_list:
        new_zip.write(name) // записали 

// для существующего
with zipfile.ZipFile('new.zip', 'a') as new_zip: // a - append mode
     new_zip.write('data.txt')
     new_zip.write('latin.txt')

```
Легкое создание
```c
import shutil

# shutil.make_archive(base_name, format, root_dir)
shutil.make_archive('data/backup', 'zip', 'data/')
shutil.unpack_archive('backup.tar', 'extract_dir/') //extract
```

