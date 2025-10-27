FROM python:3.13-slim

# Минимальные системные зависимости для сборки psycopg2 и др.
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка Poetry
RUN pip install --no-cache-dir poetry

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .


EXPOSE 8000

# Запуск через Gunicorn (production-ready)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]