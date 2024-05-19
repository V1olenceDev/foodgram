# Foodrgam

> Продуктовый помощник - проект курса Python-разработчик Плюс. Проект представляет собой онлайн-сервис, в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии проекта

- Django — веб-фреймворк для разработки веб-приложений.
- DjangoRestFramework — фреймворк для создания API.
- Docker — платформа для автоматизации развёртывания приложений в контейнерах.
- Redoc — инструмент для создания документации к API.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

### Как запустить проект:

Клонируйте репозиторий и перейдите в него в командной строке:

```
git clone git@github.com:V1olenceDev/foodgram.git
```

```
cd foodgram
```

Cоздайте и активируйте виртуальное окружение:

```
python -m venv venv
```

```
. venv/Scripts/activate
```

Установите зависимости из файла `requirements.txt`:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Установите на сервере `docker` и `docker-compose`.

Создайте файл `.env`  в корне проекта. Шаблон для заполнения файла:

```
SECRET_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ALLOWED_HOSTS=XXX.XXX.XX.XX,localhost,127.0.0.1,foodgram-gasp2023.bounceme.net
DEBUG=True
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
DB_ENGINE=django.db.backends.postgresql
```

Выполните команду 

```
docker-compose up -d --build
```

Выполните миграции 

```
docker-compose exec backend python manage.py migrate
```

Создайте суперюзера 

```
docker-compose exec backend python manage.py createsuperuser
```

Соберите статику 

```
docker-compose exec backend python manage.py collectstatic --no-input
```

Заполните базу ингредиентами

```
docker-compose exec backend python manage.py load_to_db
```

```
docker-compose exec backend python manage.py load_tags
```

Документация к API находится по адресу: <http://localhost/api/docs/redoc.html>

## Автор
[Гаспарян Валерий Гургенович](https://github.com/V1olenceDev)
