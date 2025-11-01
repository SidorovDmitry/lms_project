# 🎓 LMS Project — Learning Management System API

REST API для образовательной платформы с поддержкой курсов, уроков и системы оплаты.

---

## 📌 Возможности

- ✅ Регистрация и вход по **email** (без username)
- 📖 Полное управление **курсами** и **уроками** (CRUD)
- 💳 Система **платежей** за курсы или отдельные уроки
- 🔍 Фильтрация платежей по курсу, уроку и способу оплаты
- 🖼️ Загрузка аватаров и превью изображений

---

## 🛠 Технологии

- Python 3.13+
- Django 5.2+
- Django REST Framework
- Poetry (управление зависимостями)
- PostgreSQL
- Redis
- Celery
- Docker & Docker Compose

---

## 📁 Структура проекта
```commandline
lms_project/
│
├── config/                     # 📁 Настройки Django проекта
│   ├── __init__.py
│   ├── asgi.py                 # 🌐 ASGI конфигурация
│   ├── celery.py               # ⚙️ Celery конфигурация
│   ├── settings.py             # ⚙️ Основные настройки
│   ├── urls.py                 # 🧭 Главные URL маршруты
│   └── wsgi.py                 # 🖥️ WSGI конфигурация
│
├── materials/                  # 📁 Приложение: учебные материалы
│   ├── migrations/             # 🔄 Миграции базы данных
│   ├── __init__.py
│   ├── admin.py                # 👮 Админ-панель
│   ├── apps.py                 # 🏷️ Конфигурация приложения
│   ├── models.py               # 🗃️ Модели данных
│   ├── serializers.py          # 📤 Сериализаторы DRF
│   ├── tests.py                # 🧪 Тесты
│   ├── urls.py                 # 🔗 URL маршруты
│   └── views.py                # 🖼️ Представления
│
├── payments/                   # 📁 Приложение: платежи
│   ├── migrations/             # 🔄 Миграции базы данных
│   ├── __init__.py
│   ├── admin.py                # 👮 Админ-панель
│   ├── apps.py                 # 🏷️ Конфигурация приложения
│   ├── models.py               # 🗃️ Модели данных
│   ├── serializers.py          # 📤 Сериализаторы DRF
│   ├── tests.py                # 🧪 Тесты
│   ├── urls.py                 # 🔗 URL маршруты
│   └── views.py                # 🖼️ Представления
│
├── users/                      # 📁 Приложение: пользователи
│   ├── migrations/             # 🔄 Миграции базы данных
│   ├── __init__.py
│   ├── admin.py                # 👮 Админ-панель
│   ├── apps.py                 # 🏷️ Конфигурация приложения
│   ├── models.py               # 🗃️ Модели данных
│   ├── serializers.py          # 📤 Сериализаторы DRF
│   ├── tests.py                # 🧪 Тесты
│   ├── urls.py                 # 🔗 URL маршруты
│   └── views.py                # 🖼️ Представления
│
├── media/                      # 📁 Медиа файлы
├── .env                        # 🔐 Переменные окружения
├── .env.sample                 # 📝 Пример переменных окружения
├── .dockerignore               # 🚫 Исключения для Docker
├── docker-compose.yml          # 🐳 Docker Compose конфигурация
├── Dockerfile                  # 🐳 Docker образ
├── manage.py                   # 🛠️ Утилита управления Django
├── poetry.lock                 # 🔒 Зависимости Poetry
├── pyproject.toml              # 📦 Конфигурация Poetry
├── requirements.txt            # 📜 Зависимости pip
├── swagger.json                # 📚 Документация API
└── README.md                   # 📘 Документация
```
---

## 🐳 Быстрый запуск через Docker

### Требования
- Docker
- Docker Compose

### 1. Клонируйте репозиторий

```bash
  git clone https://github.com/SidorovDmitry/lms_project
  cd lms_project
```

### 2. Настройте окружение
```bash
  cp .env.sample .env
```
Отредактируйте .env при необходимости.
### 3. Запустите проект
```bash
  docker-compose up --build
```
Проект будет доступен по адресу: http://localhost:8000

---
## 🔍 Проверка работоспособности сервисов

### 1. ✅ Django приложение
- URL: http://localhost:8000

- Проверка: Откройте в браузере, должна появиться стартовая страница Django

- Админка: http://localhost:8000/admin (после создания суперпользователя)

### 2. 🗄️ База данных PostgreSQL
- Порт: 5432

- Проверка:

```bash
  # Подключитесь к контейнеру
docker exec -it lms_project_db psql -U postgres -d lms

# Выполните команду
\l  # список баз данных
\dt # список таблиц
```
### 3. 🔴 Redis
- Порт: 6379
- Проверка:

```bash
# Подключитесь к Redis
docker exec -it lms_redis redis-cli

# Проверьте подключение
ping  # должен ответить PONG
```

### 4. 📧 MailHog (тестирование email)r

- Web UI: http://localhost:8025
- SMTP порт: 1025
- Проверка: Откройте веб-интерфейс для просмотра отправленных email

### 5. ⚙️ Celery Worker

- Проверка:

```bash
# Проверьте логи
docker-compose logs celery-worker

# Должны быть сообщения о успешном запуске:
# celery@<container_id> ready
```

### 6. ⏰ Celery Beat

- Проверка:

```bash
# Проверьте логи
docker-compose logs celery-beat

# Должны быть сообщения о запуске планировщика
```

### 🛠 Полезные команды Docker
Работа с контейнерами

``` bash
# Запуск в фоновом режиме
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Просмотр логов конкретного сервиса
docker-compose logs web
docker-compose logs db
docker-compose logs celery-worker

# Пересборка и запуск
docker-compose up --build

# Остановка с удалением volumes
docker-compose down -vа
```

### Администрирование
```bash
# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Выполнение миграций
docker-compose exec web python manage.py migrate

# Сбор статических файлов
docker-compose exec web python manage.py collectstatic

# Создание миграций
docker-compose exec web python manage.py makemigration
```

### 🔧 Настройка переменных окружения
Создайте файл .env на основе .env.sample:

```
SECRET_KEY=

DEBUG=

POSTGRES_DB_NAME=
POSTGRES_DB_PASSWORD=
POSTGRES_DB_USER=
POSTGRES_DB_HOST=
POSTGRES_DB_PORT=

STRIPE_SECRET_KEY=

CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
CELERY_BEAT_SCHEDULER=r

REDIS_URL=

EMAIL_BACKEND=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_USE_TLS=
EMAIL_USE_SSL=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```
## 🚀 Ручная установка (без Docker)




### 1. Установите зависимости через Poetry
``` bash
  poetry install
```
### 2. Активируйте виртуальное окружение
``` bash
  poetry shell
```

### 3. Настройте окружение
``` bash
  cp .env.sample .env
```
Заполните .env актуальными значениями

### 4. Примените миграции

``` bash
  python manage.py migrate
```


### 5. Создайте суперпользователя (опционально)

``` bash
   python manage.py createsuperuser
```


### 6. Запустите сервер

``` bash
  python manage.py runserver
```

API будет доступно по адресу: http://127.0.0.1:8000/api/


## 📚 Документация API
Документация API доступна через Swagger:

- Swagger UI: http://localhost:8000/swagger/
- JSON документация: swagger.json
- 
Для получения дополнительной информации обратитесь к [документации](docs/README.md).

---
## 📚🧪 Тестирование
### Запуск тестов

``` bash

# Все тесты
docker-compose exec web python manage.py test

# Конкретное приложение

docker-compose exec web python manage.py test materials

# С покрытием кода
docker-compose exec web python manage.py test --coverage
```
---
## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).




<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Roboto+Mono&weight=600&size=26&duration=3000&pause=1000&color=36BCF7&background=FFFFFF00&center=true&width=600&lines=Dmitriy+Sidorov;Python+Developer+%7C+Django;Django+REST+%7C+Docker+%7C+Git;Welcome+to+my+profile!+%F0%9F%91%8B">
</p>