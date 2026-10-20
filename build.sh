#!/usr/bin/env bash
# Скрипт сборки для Render

set -o errexit

# 1. Установка зависимостей
pip install -r requirements.txt

# 2. Сбор статических файлов
python manage.py collectstatic --no-input

# 3. Применение миграций
python manage.py migrate