# Foodrgam

 Продуктовый помощник - проект курса Python-разработчик Плюс. Проект представляет собой онлайн-сервис в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект реализован на `Django` и `DjangoRestFramework`. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием `Redoc`.

## Особенности реализации

- Проект завернут в Docker-контейнеры;
- Образы foodgram_frontend, foodgram_backend и foodgram_gateway запушены на DockerHub;
- Реализован workflow c автодеплоем на удаленный сервер и отправкой сообщения в Telegram;
- Проект ранее был развернут на сервере: <http://foodgram-gasp2023.bounceme.net/>
- Данные админки для тестирования:
<p style="text-indent: 40px;">Логин: `V1`</p>
<p style="text-indent: 40px;">Пароль: `Valerka0099`</p>

## Развертывание проекта

### Развертывание на локальном сервере

1. Установите на сервере `docker` и `docker-compose`.
2. Создайте файл `.env`  в корне проекта. Шаблон для заполнения файла:

   <p style="text-indent: 40px;">`SECRET_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"`</p>
   <p style="text-indent: 40px;">`ALLOWED_HOSTS=XXX.XXX.XX.XX,localhost,127.0.0.1,foodgram-gasp2023.bounceme.net`</p>
   <p style="text-indent: 40px;">`DEBUG=True`</p>
   <p style="text-indent: 40px;">`POSTGRES_DB=foodgram`</p>
   <p style="text-indent: 40px;">`POSTGRES_USER=foodgram_user`</p>
   <p style="text-indent: 40px;">`POSTGRES_PASSWORD=foodgram_password`</p>
   <p style="text-indent: 40px;">`DB_NAME=foodgram`</p>
   <p style="text-indent: 40px;">`DB_HOST=db`</p>
   <p style="text-indent: 40px;">`DB_PORT=5432`</p>
   <p style="text-indent: 40px;">`DB_ENGINE=django.db.backends.postgresql`</p>
3. Выполните команду `docker-compose up -d --buld`.
4. Выполните миграции `docker-compose exec backend python manage.py migrate`.
5. Создайте суперюзера `docker-compose exec backend python manage.py createsuperuser`.
6. Соберите статику `docker-compose exec backend python manage.py collectstatic --no-input`.
7. Заполните базу ингредиентами `docker-compose exec backend python manage.py load_to_db`; `docker-compose exec backend python manage.py load_tags`
8. **Для корректного создания рецепта, необходимо создать пару тегов в базе через админку.**
9. Документация к API находится по адресу: <http://localhost/api/docs/redoc.html>.

## Автор

 Гаспарян Валерий (gasparyan.valeri@yandex.ru)


