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