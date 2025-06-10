# Django Shop

Учебный интернет-магазин на Django. Проект выполняется поэтапно в рамках курса, с соблюдением GitFlow.

## Установка

1. Клонировать репозиторий:

```bash
git clone https://github.com/GVia93/Django_shop.git
cd Django_shop
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Запустить сервер:

```bash
python manage.py runserver
```

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
