# Описание задачи

_Нужно спарсить артикулы всех товаров продавца на сайте WildBerries и записать их в базу данных._

_UPD: задача выполнена, разширение ТЗ:_

_Нужно спарсить цену и имеющиеся размеры, если это одежда._

_UPD: задача выполнены и парсер готов. Теперь следующее - перепись код, но теперь парсинг будет происходить через запрос и получение ответа в json._

_Из данных + райтинг и кол-во отзывов_

______________________________________________________________________________________________________________________________

_I need to parse the articles of all the seller's products on the WildBerries website and write them to the database_

_UPD: the task is completed, the expansion of the Technical task_

_You need to parse the price and the available sizes, if it's clothes._

_UPD: the task is completed and the parser is ready. Now the following is a rewrite of the code, but now parsing will occur through a request and receiving a response in json._

_From the data + rating and number of reviews_


# Версия 0.1 (Version 0.1)

## Особенности (Features)

1. Программа разбита на функции (The program is divided into functions)
2. Требуется пользователь для ввода кол-во страниц (A user is required to enter the number of pages)

# Версия 0.2 (Version 0.2)

## Особенности (Features)

1. Пользователь не нужен, скрпит полностью автоматизирован (The user is not needed, the script is fully automated)
2. Функции отсутствуют (There are no functions)

# Версия 0.3 (Version 0.3)

## Особенности (Features)
1. Код выглядит опрятнее засчёт разбивки на функции (The code looks neater due to the breakdown into functions)
2. Теперь html код хранится в переменной, а не в файле (Now the html code is stored in a variable, not in a file)
3. Добавили wait, чтобы ждать ровно столько, сколько требуются для загрузки страницы (Added wait to wait exactly as long as it takes to load the page)

# Версия 0.4 (Version 0.4)

## Особенности (Features)
1. Привязали к базе данных, переменные из листа идут сразу туда (Connected to the database, variables from the sheet go directly there)

# Версия 0.5 (Version 0.5)

## Особенности (Features)
1. Работа с MySql происходит с помощью модуль pymysql (Working with MySQL is done using the pymysql module)
2. Привязка к бд теперь в отдельной функции (Connecting to the database is now in a separate function)
3. Теперь при выполнении скрипта окна браузера не открываются ( Now, when executing the script, browser windows do not open)

## Версия 0.5 является MVP проекта, она также соответсвует изначально заявленому ТЗ. Далее обозначение версий будет начинаться с единицы. 

## (Version 0.5 is the MVP of the project, it also corresponds to the originally stated TK. Further, the designation of versions will begin with one)

# Версия 1.0 (Version 1.0)

## Особенности (Features)
1. Парсинг цен (Price parsing)

# Версия 1.1 (Version 1.1)

## Особенности (Features)
1. Создан лог в котором ведётся отчёт выполнение скрипта, обработка ошибок (A blog has been created in which the script execution, error handling report is maintained)
2. Новые функции для читаемости (New features for readability)

# Версия 1.2 (Version 1.2)

## Особенности (Features)
1. Парсинг размеров (Size parsing)

## Версия 1.2 является завершающей версией парсера по его изначальной задумке. Далее версии буду начинатся с 2.0

## Version 1.2 is the final version of the parser according to its original idea. Further versions will start with 2.0

# Версия 2.0 (Version 2.0)

## Особенности (Features)
1. Парсинг через requests и json (Parsing via requests and json)
2. Функции (Functions)

# Версия 2.1 (Version 2.1)

## Особенности (Features)
1. Выгрузка в бд (Uploading to the database)
2. Лог для остлеживания процессов программы (Log for tracking program processes)

## Версия 2.1 является завершающей версией парсера через JSON

## Version 2.1 is the final version of the parser via JSON





