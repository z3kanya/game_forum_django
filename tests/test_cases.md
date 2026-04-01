# Тест-кейсы: регистрация пользователя

## ТС-001: Успешная регистрация

### Предусловия: нет пользователя с такими данными

### Шаги:
1. POST /api/core/register/
2. Body: { "username": "testuser1", "email": "test1@example.com", "password": "TestPass123", "password2": "TestPass123" }

### Ожидаемые результаты: статус 201, в ответе id, username, email

### Фактический результат: 201 status
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
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc1NjY4NjA1LCJpYXQiOjE3NzUwNjM4MDUsImp0aSI6IjFiZGJkZDVjOTIxNTQwNDg5YTEwMmUwMmNmOGY5Y2ExIiwidXNlcl9pZCI6IjExIn0.kThI_Il2olXZmJ0_WqAvDmqItIVqXQPb5v-pHxQiPCM"
}

### Статус: pass

