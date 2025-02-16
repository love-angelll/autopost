# Базовый образ с Python
FROM python:3.9-slim

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование файла requirements.txt для установки зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов приложения
COPY ./main/* .

# Команда для запуска приложения
CMD ["python", "main.py"]
