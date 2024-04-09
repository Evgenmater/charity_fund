### Приложение для Благотворительного фонда

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на корм оставшимся без попечения кошкам/собакам — на любые цели, связанные с поддержкой кошачьей/собачей популяции.

### Как запустить проект:

* Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Evgenmater/charity_fund.git
```

```
cd charity_fund
```

* Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

* Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

* Перед запуском проека надо создать файл .env и внести данные для автоматическое создание первого суперюзера:

```
FIRST_SUPERUSER_EMAIL = "почтовый адрес"
FIRST_SUPERUSER_PASSWORD = "пароль для аккаунта"
```

* Запустить проект(--reload для автоматического обновления, после сохранения каких-либо изменений):

```
uvicorn app.main:app --reload
```

Примеры запросов к API:

* GET-запрос для получения списка всех благотворительных проектов.

    ```
    http://127.0.0.1:8000/charity_project
    ```
* POST-запрос для создания благотворительного проекта(Доступно только суперюзерам).

    ```
    http://127.0.0.1:8000/charity_project
    ```
* Остальную информацию можно посмотреть в docs.

    ```
    http://127.0.0.1:8000/docs
    ```

### Автор:  
Хлебнев Евгений Юрьевич<br>
**email**: hlebnev@yandex.ru<br>
**telegram** @Evgen0991