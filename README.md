# Апишка

Для начала нужна регистрация. 
## /register
### POST
```json   
{
    'username': 'text',
    'email': 'text',
    'password': 'text',
    'sex': 'text', # Мужской/Женский
    'birthday': 'YYYY-MM-DD',
    'address': 'text',
}
```
Вернет те же данные.
## /login
### POST
```json
{
  "username": "text",
  "password": "text"
}
```
Вернет
```json
{
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjczNTczNDQ3LCJpYXQiOjE2NjgzODk0NDd9.i1GoAl-TgkXUVlQdhoxHJhk8QDaBxf_8YC0nXGFvKiA"
}
```

## /logout
### POST
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjczNTczNDQ3LCJpYXQiOjE2NjgzODk0NDd9.i1GoAl-TgkXUVlQdhoxHJhk8QDaBxf_8YC0nXGFvKiA"
}
```



# Использование короче. 
Всегда добавляешь к своим GET/POST запросам вот такую шнягу:
```json
{
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjczNTczNDQ3LCJpYXQiOjE2NjgzODk0NDd9.i1GoAl-TgkXUVlQdhoxHJhk8QDaBxf_8YC0nXGFvKiA"
}
```
## /user
Информация о собственном профиле пользователя
### GET
```json
{
    "id": 2,
    "username": "vsky",
    "email": "vsky@mail.ru",
    "address": "Бебринск ул. Пушкина д. Колотушника",
    "sex": "Мужской",
    "birthday": "2004-02-28",
    "date_joined": "2022-11-13T23:29:19.119937Z"
}
```
## /user/get
### GET
Возвращает информацию о конкретном пользователе. 

Добавляешь в запрос с JWT такое:
```json
{
  'id': "2", #1,3,4
}
```
Вовзращает
```json
{
    "id": 2,
    "username": "vsky",
    "email": "vsky@mail.ru",
    "address": "Бебринск ул. Пушкина д. Колотушника",
    "sex": "Мужской",
    "birthday": "2004-02-28",
    "date_joined": "2022-11-13T23:29:19.119937Z"
}
```

## /users
### GET
Вывод всех зарегистрированных пользователей

Возвращает
```json
[
    {
        "id": 1,
        "username": "vsky_adm",
        "email": "vsky@vsky.ru",
        "address": "ывавыаыв",
        "sex": "Мужской",
        "birthday": "2004-02-28",
        "date_joined": "2022-11-13T23:10:26.653335Z"
    },
    {
        "id": 2,
        "username": "vsky",
        "email": "vsky@mail.ru",
        "address": "Бебринск ул. Пушкина д. Колотушника",
        "sex": "Мужской",
        "birthday": "2004-02-28",
        "date_joined": "2022-11-13T23:29:19.119937Z"
    }
]
```

# Лента
## /posts
### GET
Возвращает все посты
```json
[
    {
        "post_title": "Моя первая любовь",
        "post_text": "Че думали питон? Пффф",
        "pub_date": "2022-11-14T04:07:32.287380Z",
        "post_author": 2
    },
    {
        "post_title": "Моя вторая любовь",
        "post_text": "Че думали питон? Пффф",
        "pub_date": "2022-11-14T04:19:13.635879Z",
        "post_author": 2
    }
]
```
## /posts/create
### POST
Создать пост

Передаешь вместе с JWT
```json
{
  "post_title": "Моя вторая любовь",
  "post_text": "Кодинг в 5 утра ааааа",
}
```
Возвращает созданный пост
```json
{
    "post_title": "Моя вторая любовь",
    "post_text": "Кодинг в 5 утра ааааа",
    "pub_date": "2022-11-14T04:19:13.635879Z",
    "post_author": 2
}
```

# Комментарии к постам в ленте
## /comments
### GET
Возвращает комментарии к посту

Передаешь вместе с JWT:
```json
{
  "post_id": 1
}
```
Возвращает
```json
[
    {
        "post": 1,
        "comment_text": "Лол. Кек. Чебурек!",
        "comment_author": 2,
        "pub_date": "2022-11-14T04:47:22.074278Z"
    }
]
```

## /comments/leave
### POST
Оставить комментарий.

Передаешь вместе с JWT:
```json
{
  "post_id": 1,
  "comment_text": "Лол. Кек. Чебурек!",
}
```
Возвращает созданный коммент
```json
{
    "post": 1,
    "comment_text": "Лол. Кек. Чебурек!",
    "comment_author": 2,
    "pub_date": "2022-11-14T04:47:22.074278Z"
}
```

# Услуги
## /requests
### GET
Возвращает список всех заказанных услуг для ЖКХ.
```json
[
    {
        "customer": 2,
        "service_type": "Вызов сантехника",
        "customer_comment": "Течет труба на 6 этаже",
        "pub_date": "2022-11-14T05:08:00.647272Z",
        "status": false,
        "status_comment": "Отправлена"
    }
]
```
## /requests/create
### POST
Запросить услугу. 

Передаешь вместе с JWT:
```json
{
  "service_type": "Вызов сантехника",
  "customer_comment": "Течет труба на 6 этаже",
}
```
Возвращает созданную заявку.
```json
{
    "customer": 2,
    "service_type": "Вызов сантехника",
    "customer_comment": "Течет труба на 6 этаже",
    "pub_date": "2022-11-14T05:08:00.647272Z",
    "status": false,
    "status_comment": "Отправлена"
}
```

## /requests/my
### GET
Список заявок пользователя

Возвращает
```json
[
    {
        "customer": 2,
        "service_type": "Вызов сантехника",
        "customer_comment": "Течет труба на 6 этаже",
        "pub_date": "2022-11-14T05:08:00.647272Z",
        "status": false,
        "status_comment": "Отправлена"
    }
]
```
