# Django Shop

Учебный интернет-магазин на Django. Разрабатывается поэтапно в рамках курса, с соблюдением GitFlow и PostgreSQL.

## Установка

```bash
git clone https://github.com/GVia93/Django_shop.git
cd django-shop
python -m venv venv
pip install -r requirements.txt
```

## Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your_secret_key
DEBUG=True

NAME=django_shop
USER=postgres
PASSWORD=your_password
HOST=localhost
PORT=5432
```

## Запуск

```bash
python manage.py runserver
```

## Основные модели

### Category
- name — наименование
- description — описание

### Product
- name — наименование
- description — описание
- image — изображение
- category — связь с Category
- price — цена
- created_at / updated_at — временные метки

## Кастомные команды

```bash
python manage.py load_test_data
```
Удаляет старые данные и создаёт тестовые категории и продукты.

## Структура проекта

- `catalog/` — приложение с маршрутами, шаблонами и контроллерами
- `config/` — конфигурация проекта
- `templates/` — HTML-шаблоны
- `static/` — Bootstrap и статические файлы

## Маршруты

| Адрес             | Описание                |
|-------------------|-------------------------|
| `/`               | Главная страница        |
| `/contacts/`      | Страница с контактами   |
