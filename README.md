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
- PostgreSQL (по умолчанию)

---

## 📁 Структура проекта
```commandline
lms_project/
├── config/               # Настройки Django (settings, urls, asgi, wsgi)
├── materials/            # Курсы и уроки
│   ├── migrations/
│   ├── models.py         # Course, Lesson
│   ├── serializers.py    # CourseSerializer, LessonSerializer
│   ├── views.py          # CourseViewSet, LessonListCreateView и др.
│   └── urls.py           # URL-маршруты для materials
├── users/                # Пользователи и платежи
│   ├── migrations/
│   ├── models.py         # User, Payment
│   ├── filters.py        # PaymentFilter
│   ├── serializers.py    # UserSerializer, PaymentSerializer
│   ├── views.py          # PaymentViewSet
│   └── admin.py          # Регистрация моделей в админке
├── .env                  # Переменные окружения
├── .env.sample           # Шаблон переменных
├── .gitignore            # Исключения для Git
├── manage.py             # Утилита управления проектом
├── poetry.lock           # Зафиксированные версии пакетов
├── pyproject.toml        # Конфигурация Poetry
└── README.md             # Документация проекта 
```
## 🚀 Установка и запуск

### 1. Клонируйте репозиторий

git clone https://github.com/SidorovDmitry/lms_project


### 2. Установите зависимости через Poetry
Зависимости проекта управляются через Poetry. Они перечислены в файле `pyproject.toml`

### 3. Настройте окружение
Создайте файл .env на основе шаблона:`.env.sample `

Заполните его актуальными значениями.

### 4. Примените миграции

`poetry run python manage.py migrate`


### 5. Создайте суперпользователя (опционально)

`poetry run python manage.py createsuperuser`


### 6. Запустите сервер

`poetry run python manage.py runserver`

API будет доступно по адресу: http://127.0.0.1:8000/api/


## Документация:
Для получения дополнительной информации обратитесь к [документации](docs/README.md).

## Лицензия:

Этот проект лицензирован по [лицензии MIT](LICENSE).




<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Roboto+Mono&weight=600&size=26&duration=3000&pause=1000&color=36BCF7&background=FFFFFF00&center=true&width=600&lines=Dmitriy+Sidorov;Python+Developer+%7C+Django;Django+REST+%7C+Docker+%7C+Git;Welcome+to+my+profile!+%F0%9F%91%8B">
</p>