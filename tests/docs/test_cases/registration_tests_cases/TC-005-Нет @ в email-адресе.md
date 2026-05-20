## ТС-005: Некорректный email при регистрации (нет @ в email-адресе)

### Предусловия:
- Пользователь с данными отсутствует.

### Шаги:
1. POST `/api/core/register/`
2. Тело:
   {
       "username": "testuser6",
       "email": "test6example.com",
       "password": "TestPass123",
       "password2": "TestPass123"
   }

### Ожидаемые результаты: 
- статус 400
- в ответе ошибка, сообщающая о некорректном email