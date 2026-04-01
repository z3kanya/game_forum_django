# Game News Web Service

Веб-сервис для новостей по играм с возможностью скачивания через torrent и системой уведомлений.

## Технологический стек

- **Backend**: Django 4.2.7 + Django REST Framework
- **Database**: SQLite3
- **Frontend**: HTML + CSS + JS / React (опционально)
- **Architecture**: REST API + SOLID principles
- **Structure**: Modular (module-based)

## Структура проекта

```
project_group_python/
├── config/                 # Основные настройки проекта
│   ├── __init__.py
│   ├── settings.py         # Настройки Django
│   ├── urls.py            # Главные URL маршруты
│   ├── wsgi.py            # WSGI конфигурация
│   └── asgi.py            # ASGI конфигурация
├── apps/                   # Модули приложения
│   ├── core/              # Базовый модуль (пользователи, общие модели)
│   ├── news/              # Модуль новостей по играм
│   ├── torrents/          # Модуль торрентов
│   └── notifications/     # Модуль уведомлений
├── static/                 # Статические файлы (CSS, JS, изображения)
├── media/                  # Медиа файлы (загруженные пользователями)
├── templates/              # HTML шаблоны (если не используется только React)
├── frontend/               # React приложение (опционально)
├── requirements.txt        # Зависимости Python
├── manage.py              # Django управляющий скрипт
└── README.md              # Документация

```

## Модули проекта

### 1. Core (apps/core/)
Базовый модуль, содержащий:
- Модели пользователей (если нужна кастомная модель)
- Общие утилиты и базовые классы
- Общие сериализаторы и представления

### 2. News (apps/news/)
Модуль новостей по играм:
- CRUD операции для новостей
- Категории новостей
- Поиск и фильтрация
- Комментарии к новостям

### 3. Torrents (apps/torrents/)
Модуль для работы с торрентами:
- Загрузка и управление торрент-файлами
- Статистика загрузок
- Интеграция с libtorrent

### 4. Notifications (apps/notifications/)
Модуль уведомлений:
- Email уведомления
- Настройки подписок
- История уведомлений

## Архитектурные принципы

### REST API
- Все API endpoints следуют RESTful принципам
- Использование Django REST Framework
- Документация API через drf-spectacular

### SOLID принципы
- **Single Responsibility**: Каждый модуль отвечает за свою область
- **Open/Closed**: Легко расширять без изменения существующего кода
- **Liskov Substitution**: Правильное использование наследования
- **Interface Segregation**: Разделение интерфейсов на более мелкие
- **Dependency Inversion**: Зависимость от абстракций, а не от конкретных реализаций

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Примените миграции:
```bash
python manage.py migrate
```

4. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

5. Запустите сервер:
```bash
python manage.py runserver
```

## Разработка

### Создание миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### Запуск тестов
```bash
python manage.py test
```

## Документация

Полная документация проекта доступна в папке `docs/`:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Описание архитектуры и принципов проектирования
- **[MODULES.md](docs/MODULES.md)** - Детальное описание модулей и задач
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Руководство по разработке
- **[PROJECT_EVALUATION.md](docs/PROJECT_EVALUATION.md)** - Оценка проекта и рекомендации по улучшению
- **[FEATURE_ROADMAP.md](docs/FEATURE_ROADMAP.md)** - Roadmap дополнительных функций

## Оценка проекта

**Текущая концепция: 8/10 ⭐**

Проект имеет отличную архитектурную базу и хорошо подходит для первого командного проекта.

### Сильные стороны:
- ✅ Четкое разделение на модули (SOLID)
- ✅ RESTful API структура
- ✅ Современный стек технологий
- ✅ Практическая направленность

### Рекомендуемые дополнения:
1. **Аутентификация** (JWT) - критически важно для MVP
2. **Система рейтингов** (лайки, избранное) - увеличивает вовлеченность
3. **Расширенный поиск** - улучшает UX
4. **Комментарии с threading** - формирует сообщество
5. **Аналитика** - показывает навыки работы с данными

Подробнее см. [PROJECT_EVALUATION.md](docs/PROJECT_EVALUATION.md)

## Опциональные зависимости

Для расширенного функционала есть файл `requirements-optional.txt`:
```bash
pip install -r requirements-optional.txt
```

Включает зависимости для:
- Работы с изображениями (Pillow)
- WebSocket (Channels)
- Кеширования (django-redis)
- Тестирования (pytest)
- И других функций



### Docker compose:

### Запуск и остановка

docker compose up -d                # запустить в фоне
docker compose up -d --build        # пересобрать образ и запустить
docker compose down                 # остановить (данные БД сохранятся)
docker compose down -v              # остановить и удалить тома (сброс БД)
docker compose restart web          # перезапустить только веб-контейнер

### Логи и статус

docker compose ps                   # статус контейнеров
docker compose logs -f web          # следить за логами веб-контейнера
docker compose logs -f db           # следить за логами БД


### Команды внутри контейнера (миграции, shell и т.д.)

docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell
docker compose exec web sh           # войти в оболочку контейнера