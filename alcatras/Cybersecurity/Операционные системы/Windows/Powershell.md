
 #### ***cmd***
Есть встроенные команды, например DIR, для которых нет собственного бинарника, а есть команды с бинарником - ipconfig, например.  cmd очень ограничен поскольку вывод каждой команды это просто текст. 
#### **powershell**
powershell полностью работает с объектами .NET.  **.NET** это короче фреймворк, который позволяет программистам меньше писать кода. На Windows .NET работает с обьектами -> powershell работает с обьектами -> проблема с plain text решается. Внутри себя .NET ссылается на Win32API

$PSVersionTable - узнать версию
Get-ChildItem Env:  -  посмотреть переменные среды
##### **Execution Policy**
Короче когда скрипт сохранен, как файл, то по умолчанию его нельзя просто запустить. 
> Get-ExecutionPolicy - получить политику выполнения
> Set-ExecutionPolicy RemoteSigned/Restricted  -  [тык](https://learn.microsoft.com/ru-ru/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.6)****

Короче как я понял лучше всего использовать RemoteSigned  - он требует, чтобы скрипты  скачанные с интернета были подписаны. 

## Help System
Update-Help- обновление системы. 
#### Get-Help

```

1. Get-Help -Name(можно без) Get-Process -Full(полная информация) - аналог man для каждой команды.
Get-Help \[Name] -Online -  это все то же самое только читать не в консоли, а на нормальном сайте.
Или можно просто help Get-Process  - то же самое.
help Get-Process -Parameter ComputerName  - help по конкретному параметру
help Get-Process | Out-GridView - посмотреть в отдельном окне
help *process* - поиск процессов - типо обычные регулярки
help *about - выведет все about страницы - доп информация к обычному help 
```
Параметры выглядят странно, но фактически это все возможные наборы, поскольку наличие 1 параметра может исключать другой и наоборот. 
![[Pasted image 20260827181606.png]]

#### Get-Command
Эта команда помогает искать другие команды
Все команды в powershell представлены, как  \<verb>-\<noun>. 
```
Get-Command -Noun Process - пример работы. 
Get-Command-Name *service* - c *
```

### **Comparison Operators***

Чтобы включить case-sensetive ***-ceq*** - добавляем c в начале каждой штуки. 
![[Pasted image 20260829203042.png]]

```
contains, in - поиск элемента в массиве, для строк не работает ----->
$number = 1..10
PS C:\Users\0987a> $number -contains 0
False
```
## Objects, Properties, and Methods

```
Get-NetTCPConnection, **`Get-NetUDPEndpoint`**.
Get-Service -Name w32time // получить сервис(очев)
Get-Process // получить список процессов
Get-Service -Name w32time | Select-Object -Property CanPauseAndContinue // получаем конкретное свойство обьекта.
Get-Service -Name w32time | Select-Object -Property * // получаем все свойства обьекта  
(Get-Service -Name w32time).GetHashCode() // вызов метода у обьекта
Get-ADUser -Identity mike- Properties * | Get-Membr // 
$Users = Get-ADUser -Identity mike -Properties * // сохранение в переменную результата команды
$MyObj = [PSCustomObject]@{ DisplayName = "Print Spooler" }
// обьявление обьекта.
Stop-Service -WhatI // безопасное тестирование 
get-childItem(ls/gci/dir) // получение обьекта ФС по строке. 
```
Не является хорошей практикой использование методов обьекта - лучше использовать специальные командлеты(кроме строковых операций). 
Пример:
```
Get-Service-Name w32time | Start-Service -PassThru // Запуск сервиса 
```
#### Get-Member
Извлечение информации об обьектах, их свойствах и методах - команды. 
```
Get-Service -Name w32time | Get-Member \[-MemberType Method] // получаем полную информацию об обьекте, который вернула команда до пайпа
```

![[Pasted image 20260828025351.png]]
Показывает не полную информацию . 

*Разница между одинарными кавычками и двойными*

![[Pasted image 20260828151333.png]]
## One-Liners and the Pipeline
one-liner - 1 непрерывный пайплайн
Можно вот так на другие строки переносить.
![[Pasted image 20260828135539.png]]
Можно вот так: 
**Переносить** после `,` , `(`, `{`, `[`, `=`, `;` (и в PowerShell после конвейера `|`).

Через ; это 2 разные несвязанные команды. 
```c
$Service = 'w32time'; Get-Service-Name $Service
```

#### Filtering left
Рекомендуется фильтровать все как можно раньше - влево, поскольку не надо будет пропускать большое количество данных через много команд. Пример как надо и как не надо
```
Get-Service-Name w32time // надо
Get-Service | Where-Object Name -eq w32time // не надо - на пайп where-object подаются лишние данные. 
```

#### The Pipeline
Есть проблема с вводом.  В help разделе INPUT написано что-то такое:
```c
INPUTS
    System.ServiceProcess.ServiceController
        You can pipe a service object to this cmdlet.
    System.String
        You can pipe a string that contains the name of a service to this cmdlet.
```
Короче надо смотреть на конкретные свойства и чекать что куда пойдет
Или так:
```
Get-MrPipelineInput -Name Stop-Service // получаем обьекты которые можно ввести
```
Будет типо вот так. 
![[Pasted image 20260828150809.png]]
Если обьект подходит во много параметров(типо у него есть имя или другие свойства, которые принимаются), то всегда сначала смотрится значение, потом имя. 

Примеры более сложных пайлайнов
```
//Эта штука берет обьект CustomObject, создает новый обьект основываясь на его свойствах, конкретно здесь извлекает свойство Service и присваивает Name и потом новый обьект с только свойством name передает на stop-service
$CustomObject | Select-Object @{label='Name';Expression={$_.Service}} | StopService

'Windows Time' | 2 Out-File-FilePath $env:TEMP\services.txt // запись в файл

Stop-Service -DisplayName (Get-Content-Path $env:TEMP\services.txt)  // достаем имена из файла с помощью Get-Content -Path и получаем и передаем в Stop-Service -DisplayName
```

#### PowerShellGet
Есть такая штука - NuGet. Грубо говоря это мененджер пакетов.  То есть пакеты структурируются и собираются по специальным правилам. Формат NuGet - nupkg. Когда много таких файлов скидывается в 1 место - NuGet репозиторий. Пример такого репозитория - **Powershell Gallery**. Там хранятся nuget пакеты -**powershell модули(готовый набор полезных инструментов, упакованных в 1 пакет)**.  
```
Find-Module -Name MrToolkit // поиск модулей. 
Find-Module -Name MrToolkit | Install-Module // установка
```

## Chapter 5
#### Форматирование 
Важно что эти команды возвращают специальный обьект: Microsoft.PowerShell.Commands.Internal.Format, а не искомый обьект.  Такие обьекты нельзя передавать в большинство обьектов. 
```
get-service * | format-table // выведет в таблице
get-service * | format-list // выведет в листе 
```
#### Aliases
Чтобы альясы существовали всегда их нужно прописывать в файл $PROFILE. 
```
Get-Alias -Name gcm // поиск команд по альасу
Get-Alias -Definition Get-Process // поиск альясов по команде
Set-Alias -Name some_name -Value // в Value можно передавать обьект function
типо вот так

"function CheckZapret { Get-Service | Where-Object Name -eq zapret }
Set-Alias -Name zapret-run-check -Value CheckZapret
"
```
#### Providers
Provider это штука, которая позволяет обращаться в разным настройкам Windows в том числе и к реестру так, как будто это просто текстовый файл. 
Сторонние модули добавляют своих Powershell провайдеров. 
```
Get-PSProvider // вывести всех провайдеров
Get-PSDrive // вывод дисков, которые используют эти провайдеры. 
Get-ChildItem -Path Function:\ // посмотреть информацию в провайдере
```

1. потому что format-list и format-table возвращают свои типы обьектов, у которых сильно урезаны возможности
2. Get-Alias -name "%"
3. потому альасы работают локально в сесиии powershell  или если прописаны в $PROFILE  только в твоем терминале
4. get-childitem Alias:
5. case-insensetive


### Chapter 6 - Scripting
Прежде чем итерировать по обьектам foreach сохраняет их в память - если обьектов много память может закончиться. 
Если обобщать то тут очень похожий на плюсовый синтаксис. 
```
 get-process -Name win* | ForEach-Object { echo ($_.Name + ": " +$_.Mainmodule.FileName); } // пример использования foreach-object
 // или так:
 
 foreach ($smth in $smth_arr) {
	 echo $smth
 }
 
 get-process | Group-Object -Property CPU | Sort-Object -Property Count -Descending
 // пример использования сортировки и группировки по свойству обьекта.
 
 
 for ($a = 0; $a -lt 4; $a++) {
	echo ($i*$i) 
} // пример работы с обычым циклом (плюсовый синтаксис)

do {
  // do something
}
until/while (condition)
  // пример работы с do/while циклами
  
while (condition) {
	//do something
	break/continue/return()
}
//
```


#### Chapter 7 - WMI/CMI(Windows Management Instrumentation)
WMI это специальная служба для администрирования Windows.  Пользовательская программа может запросить от этой службы нужную информацию об состоянии системы.  WMI дает более глубокие данные о железе и ОС и вообще просто более гибкий. 
Сейчас используется CMI для доступа к WMI, как современная кроссплатформенная замена(не используется))
```
Get-CimInstance -ClassName Win32_BIOS // немного информации о BIOS. 

Win32_OperatingSystem
Win32_ComputerSystem
Win32_LogicalDisk
Win32_Process
Win32_Service
Win32_NetworkAdapterConfiguration
Win32_BIOS

Get-CimInstance-ClassName Win32_BIOS-Property SerialNumber | 2 Select-Object -ExpandProperty SerialNumber // expandproperty вернет обычную строку

Get-CimInstance-ComputerName dc01-ClassName Win32_BIOS // dc01 - remote desktop. 

```
Нехорошая практика запускать powershell через аккаунт админа домена, например. Для этого есть CIM сессии,  

```
$CimSession = New-CimSession -ComputerName dc01 -Credential (Get-Credential) 
//мы создаем CIM сессию для компьютера dc01 и для credential используем только что созданный через get-credential обьект(должны совпадать с теми, которые зареганы на удаленной машине)
//далее используем вот так 
Get-CimInstance-CimSession $CimSession-ClassName Win32_BIOS

Get-CimSession // существующие CIM сессии.
```


## Powershell Remoting 
Между Powershell remoting и CIM remoting есть разница. Во-первых, при powershell remoting, код powershell выполняется на удаленной устройстве, а тебе назад возвращается 'снимок' обьекта. В CIM remoting тебе присылают CIM обьекты, которые Powershell сам обрабатывает.
К тому же при Powershell remoting, он очевидно должен быть запущен на обоих устройствах
```
Enable-PSRemotin // включает Remoting на устройстве. 
Set-NetConnectionProfile -InterfaceAlias Ethernet -NetworkCategory "Private" // настройка типа сети
Enter-PSSession -ComputerName dc01-Credential $Cred // one-to-one remoting
Invoke-Command -ComputerName dc01, sql02, web01 {Get-Service-Name W32time} 
-Credential $Cred // one to many remoting 

Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.1.49, DC01" -Force 
// на локальном устройстве надо добавить в Trusted Host
```
## Functions
Лучше всего использовать глаголы из *Get-Verb*
```
function Get-ACVersion { // лучше префик -> не будет конфликта
	$PSVersionTable.PSVersion 
}
```
Чтобы загрузить функцию в память, лучше всего сделать модуль, и установить его. 
```nc
1. $env:PSModulePath -split ";" 
   // узнаем где в системе лежат модули
2. mkdir (одно из того что выведет $env:PSModulePath)/ModuleName
3. notepad ModuleName.psm1
4. Туда пишем функцию
5. Import-Module ModuleName -Force
```
Можно также создать манифест
```
//Короче Path это путь до самого манифеста, psd это файл манифеста, RootModule это 
//сам скрипт. 
New-ModuleManifest -Path $env:ProgramFiles\WindowsPowerShell\Modules\MyScriptModule\MyScriptModule.psd1 -RootModule MyScriptModule -FunctionsToExport = 'Get-MrPSVersion'
//последнее позволяет через манифест определять какие функции будут видны пользователяем, а какие нет.
```
Работа с параметрами:
```
function Test-Param {
	param (
		[string[]]$parameter // хорошей практикой является типизация
	)
	echo $parameter
```

**Advanced Functions**
Такие функции отличаются от обычных тем, что у них есть стандартный набор параметров. 
Чтобы такие параметры появились нужно просто добавить вот такой блок:
![[Pasted image 20260904211205.png]]

*Дополнительные полезные штуки*
```
[CmdletBinding(SupportsShouldProcess)] 
// добавляет параметры WhatIF и Confirm 

[Parameter(Mandatory)]
$parameter
//заставляет ввести этот параметр

[ValidateNotNullOrEmpty()]
$parameter=default_value
//позволяет устанавливать значение по умолчанию, но сохраняет обязательный ввод для всего не пустого
```

***Ввод с пайпа***
Здесь немного про отличия ввода
Есть вот такой ввод: *Test-NoProcess "Alice", "Bob", "Charlie".* В таком случае функция получит массив строк и выполнится 1 раз
А есть вот такой ввод: *"Alice", "Bob", "Charlie" | Test-NoProcess*. И если в функции есть PROCESS блок, то для КАЖДОГО из объектов вызовется функция. 
```
[Parameter(Mandatory, ValueFromPipeline)]
[string[]]$ComputerName
// обьект будет приводиться к строке и пытаться встать в массив


[Parameter(Mandatory,  ValueFromPipelineByPropertyName)]
[string[]]$ComputerName
// будет парситься нужное свойство обьекта

PROCESS { // необходим для правильной асинхронной обработки
	Write-Output $ComputerName
	 // для каждого обьекта на пайпе функция выполняится 1 раз
}

BEGIN {} // определяем что то до PROCESS блока для каждого обьекта. обьекты недоступны

END {} // какая-то очистка в конце

```

***Error Handling***
Иногда программки выбрасывают исключения.  Есть терминирующие - после которых команда завершает свое выполнение, а есть нетерминирующие - после них она продолжает выполнение. 
``` 
//можно обрабатывать так, но такая конструкция не отлавливает нетерминирующие ошибки.
try {
	// do smth
}
catch {
	Write-Warning -Message "some message"
}

//чтобы нетерминирующие тоже отлавливались нужно сделать как-то так
try {
	Command -Param $Param -ErrorActionStop // останавливает даже при нет
} catch {
	Write-Warning -Message "some message"
}
```

![[Pasted image 20260904210529.png]]
## Настройка собственной AD сети дома (не закончено!!!!)
Подготовка:
```
Get-NetConnectionProfile, или так Get-NetAdapter
// получаем информацию об альясе интерфейса и сетевой категории

Get-NetIPAddress, Get-NetIPInterface
// получение подробной информации об адаптере

New-NetIPAddress -InterfaceAlias Ethernet -IPAddress 192.168.1.67 -PrefixLength 24 -DefaultGateway 192.168.1.1 
//настройка сетевого адаптера. Все параметры обязательные, поскольку с неправильной маской и без шлюза нельзя общаться по сети

Set-Item WSMan:\localhost\Client\TrustedHosts -Value "192.168.1.100" 
// добавление в TrustedIP

Set-DnsClientServerAddress
// настройка DNS 


```


AD фильтры
```
<Атрибут> <оператор> <значение> - samAccountName -eq daklik_not
```
AD команды
```
Get-ADUser -Identity laptop 
//получение информации об пользователе
Set-ADAccountPassword -Identity "laptop" -NewPassword $SecurePassword -Reset
//установка нового пароля
```



