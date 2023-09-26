# Тестовое задание в "ПроКомплаенс"
Выполнено тестовое задание в соответствии с ТЗ.

По ТЗ необходимо было реализовать сервис, позволяющий импортировать csv-файлы

## Для запуска веб-сервиса необходимо:
* Подключиться к необходимой БД PostgreSQL, заменив в settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<db_name>',
        'USER': '<username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

значения '<db_name>', '<password>' , '<username>' на значения пароля, пользователя и названия БД на локальном устройстве. 
```
* Затем находясь в директории проекта через терминал вписать
  ```
  py manage.py runserver
  ```


  ### Реализовано:
  * Авторизация пользователя
  * Получение csv-файла по его url-адресу с добавлением в БД
  * Удаление файла по его названию, присвоенному при получении через запрос
  * Получение информации о конкретном файле (Данные csv-файла)
  * Опциональная сортировка по номеру столбца
  * Получение данных из всех csv-файлов
 
  #### В качестве тестовых данных использовались:
  * https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
  * https://gist.githubusercontent.com/bobbyhadz/9061dd50a9c0d9628592b156326251ff/raw/381229ffc3a72c04066397c948cf386e10c98bee/employees.csv
  * https://www.openml.org/data/get_csv/16826755/phpMYEkMl
