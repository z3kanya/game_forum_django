## ТС-001: Успешная регистрация

### Предусловия: нет пользователя с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/register/
2. Body: { "username": "testuser3", "email": "test3@example.com", "password": "TestPass123", "password2": "TestPass123" }

### Ожидаемые результаты: статус 201, в ответе id, username, email

### Фактический результат: 201 status
{
    "success": true,
    "user": {
        "id": 44,
        "username": "testuser3",
        "email": "test3@example.com",
        "first_name": "",
        "last_name": "",
        "tg_username": null,
        "date_joined": "2026-05-11T14:22:04.196980+03:00",
        "is_moderator": false,
        "favorite_games": [],
        "avatar": null
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc5MTAzMzI0LCJpYXQiOjE3Nzg0OTg1MjQsImp0aSI6Ijc5ZmQxNzQwYzgyZjRiMmJhOTI5NzA2YTUxMWQ5OWE5IiwidXNlcl9pZCI6IjQ0In0.RKb3BrrnfxCm21xNynRH5VMe53QgsKRVTzNZnAZk8LU"
}

### Статус: pass



----------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-002: Попытка регистрации существующего пользователя

### Предусловия: есть пользователь с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/register/
2. Body: { "username": "testuser2", "email": "test2@example.com", "password": "TestPass123", "password2": "TestPass123" }

### Ожидаемые результаты: статус 400

### Фактический результат: 400 status
{
    "success": false,
    "errors": {
        "username": [
            "Пользователь с таким именем уже существует."
        ],
        "email": [
            "Пользователь с таким Email уже существует."
        ]
    }
}

### Статус: pass




----------------------------------------------------------------------------------------------------------------------------------




## ТС-003: Несовпадение паролей при регистрации

### Предусловия: нет пользователя с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/register/
2. Body: { "username": "testuser4", "email": "test4@example.com", "password": "TestPass123", "password2": "TestPass321" }

### Ожидаемые результаты: статус 400

### Фактический результат: 400 status
{
    "success": false,
    "errors": {
        "password": [
            "Пароли не совпадают"
        ]
    }
}

### Статус: pass




-----------------------------------------------------------------------------------------------------------------------------------------------




## ТС-004: Некорректный email при регистрации (нет домена первого уровня)


### Предусловия: есть пользователь с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/register/
2. Body: { "username": "testuser5", "email": "test5@example", "password": "TestPass123", "password2": "TestPass123" }

### Ожидаемые результаты: статус 400

### Фактический результат: 400 status

{
    "success": false,
    "errors": {
        "email": [
            "Введите правильный адрес электронной почты."
        ]
    }
}

### Статус: pass



------------------------------------------------------------------------------------------------------------------------------------



## ТС-005: Некорректный email при регистрации (нет @ в email-адресе)

### Предусловия: нет пользователя с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/register/
2. Body: { "username": "testuser5", "email": "test5example.com", "password": "TestPass123", "password2": "TestPass123" }

### Ожидаемые результаты: статус 400

### Фактический результат: 400 status
{
    "success": false,
    "errors": {
        "email": [
            "Введите правильный адрес электронной почты."
        ]
    }
}

### Статус: pass



------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-006: Успешный вход с корректными данными

### Предусловия: есть пользователь с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/login/
2. Body: { "username": "testuser2", "password": "TestPass123" }

### Ожидаемые результаты: статус 200

### Фактический результат: 200 status
{
    "success": true,
    "user": {
        "id": 11,
        "username": "testuser2",
        "email": "test2@example.com",
        "first_name": "",
        "last_name": "",
        "tg_username": null,
        "date_joined": "2026-04-01T20:16:44.526914+03:00",
        "is_moderator": false,
        "favorite_games": [],
        "avatar": null
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc5MTEwMzYwLCJpYXQiOjE3Nzg1MDU1NjAsImp0aSI6ImQ1ZjQ4ZGRjZTkwZDQ3NGU5MTEyYjJhNzY3ZWU5Mjk1IiwidXNlcl9pZCI6IjExIn0.cXwfSruwBhvVoKrRjgpeG3ofONbaYVzmCs7nzPa9FKo"
}

### Статус: pass



-----------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-007: Неверный пароль при входе

### Предусловия: есть пользователь с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/login/
2. Body: { "username": "testuser2", "password": "WrongPass123" }

### Ожидаемые результаты: статус 401

### Фактический результат: 500 status

### Статус: fail



------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-008: Несуществующий пользователь при входе

### Предусловия: нет пользователя с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/login/
2. Body: { "username": "nonexistentuser", "password": "123" }

### Ожидаемые результаты: статус 401

### Фактический результат: 401 status
{
    "success": false,
    "errors": "Неправильное имя пользователя или пароль"
}

### Статус: pass



------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-009: Пустые поля при входе

### Предусловия: нет пользователя с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/login/
2. Body: { "username": "", "password": "" }

### Ожидаемые результаты: статус 400

### Фактический результат: 400 status
{
    "success": false,
    "errors": "Пожалуйста, введите имя пользователя и пароль"
}

### Статус: pass



------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-010: Отсутствует поле пароль

### Предусловия: есть пользователь с такими данными, для теста используем Postman

### Шаги:
1. POST /api/core/login/
2. Body: { "username": "testuser2"}

### Ожидаемые результаты: статус 400

### Фактический результат: 400 status
{
    "success": false,
    "errors": "Пожалуйста, введите имя пользователя и пароль"
}

### Статус: pass



------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-011: Получение профиля авторизованного пользователя

### Предусловия: есть пользователь с такими данными, для теста используем Postman

### Шаги:
1. GET /api/core/profile/
2. Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc5MTEwMzYwLCJpYXQiOjE3Nzg1MDU1NjAsImp0aSI6ImQ1ZjQ4ZGRjZTkwZDQ3NGU5MTEyYjJhNzY3ZWU5Mjk1IiwidXNlcl9pZCI6IjExIn0.cXwfSruwBhvVoKrRjgpeG3ofONbaYVzmCs7nzPa9FKo


### Ожидаемые результаты: статус 200

### Фактический результат: 200 status
{
    "id": 11,
    "username": "testuser2",
    "email": "test2@example.com",
    "first_name": "",
    "last_name": "",
    "tg_username": null,
    "date_joined": "2026-04-01T20:16:44.526914+03:00",
    "is_moderator": false,
    "favorite_games": [],
    "avatar": null
}

### Статус: pass



------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-012: Получение профиля без токена (неавторизованный)

### Предусловия: нет пользователя с такими данными, для теста используем Postman

### Шаги:
1. GET /api/core/profile/

### Ожидаемые результаты: статус 403

### Фактический результат: 403 status
{
    "detail": "Учетные данные не были предоставлены."
}

### Статус: pass



------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-013: Обновление профиля - смена имени

### Предусловия: пользователь существует, для теста используем Postman

### Шаги:
1. PATCH /api/core/profile/update/
2. Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc5MTEwMzYwLCJpYXQiOjE3Nzg1MDU1NjAsImp0aSI6ImQ1ZjQ4ZGRjZTkwZDQ3NGU5MTEyYjJhNzY3ZWU5Mjk1IiwidXNlcl9pZCI6IjExIn0.cXwfSruwBhvVoKrRjgpeG3ofONbaYVzmCs7nzPa9FKo
3. Body: { "first_name": "Тестовый" }

### Ожидаемые результаты: статус 200, в ответе обновленные данные, first_name: "Тестовый"

### Фактический результат: 200 status
{
    "username": "testuser2",
    "last_name": "",
    "first_name": "Тестовый",
    "tg_username": null,
    "email": "test2@example.com",
    "avatar": null
}


### Статус: pass



------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-014: Обновление профиля - загрузка аватара

### Предусловия: пользователь существует, для теста используем Postman

### Шаги:
1. PATCH /api/core/profile/update/
2. Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc5MTEwMzYwLCJpYXQiOjE3Nzg1MDU1NjAsImp0aSI6ImQ1ZjQ4ZGRjZTkwZDQ3NGU5MTEyYjJhNzY3ZWU5Mjk1IiwidXNlcl9pZCI6IjExIn0.cXwfSruwBhvVoKrRjgpeG3ofONbaYVzmCs7nzPa9FKo
3. Body(multipart/form-data): { "avatar": "(выбрать картинку)" }

### Ожидаемые результаты: статус 200, в ответе обновленные данные, avatar: "ссылка на картинку"

### Фактический результат: 200 status
{
    "username": "testuser2",
    "last_name": "",
    "first_name": "Тестовый",
    "tg_username": null,
    "email": "test2@example.com",
    "avatar": "http://localhost:8000/media/maxresdefault_K4VleZN.jpg"
}

### Статус: pass



---------------------------------------------------------------------------------------------------------------------------------------------------------------



## ТС-015: Обновление профиля без авторизации 

### Предусловия: пользователь не авторизован, для теста используем Postman

### Шаги:
1. PATCH /api/core/profile/update/
2. Body: { "first_name": "Хакер"}

### Ожидаемые результаты: статус 401

### Фактический результат: 401 status
{
    "detail": "Учетные данные не были предоставлены."
}

### Статус: pass



---------------------------------------------------------------------------------------------------------------------------------------------------------------

