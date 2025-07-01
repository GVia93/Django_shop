# Django Shop

Учебный интернет-магазин на Django. Разрабатывается поэтапно в рамках курса, с соблюдением GitFlow и PostgreSQL.

## Возможности

- Каталог товаров с категориями
- Детальная страница товара
- Постраничный вывод товаров
- Обратная связь (форма + сообщение)
- Полноценный блог:
  - создание, просмотр, редактирование, удаление записей
  - отображаются только опубликованные статьи
  - счётчик просмотров
- Админка для управления товарами, категориями и статьями
- Использование `base.html` и `menu.html`
- Подключение Bootstrap 5

## Установка

```bash
git clone ссылка на репозитлоий
cd django_shop
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
NAME=имя_бд
USER=пользователь_бд
PASSWORD=пароль
HOST=localhost
PORT=5432
```

## Миграции и запуск

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Создание суперпользователя

```bash
python manage.py createsuperuser
```

## Кастомные команды

```bash
python manage.py load_test_data
```
Удаляет старые данные и создаёт тестовые категории и продукты.

## Структура проекта

Django_shop/
├── blog/                                                       ← приложение блога
│   ├── templates/blog/ (post_list, detail, form, delete)
│   ├── models.py, views.py, urls.py, admin.py
├── catalog/                                                    ← приложение каталога
│   ├── templates/catalog/ (home, contacts, catalog, product_detail)
│   ├── models.py, views.py, urls.py, admin.py
│   └── templates/base.html, menu.html
├── config/ (settings.py, urls.py, wsgi.py)                     ← основной проект Django
├── media/                                                      ← загружаемые файлы
├── static/                                                     ← Bootstrap и стили
├── manage.py
├── requirements.txt
├── .env
└── README.md
