from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для пользовательской модели.
    Позволяет просматривать и редактировать основную информацию
    о пользователях, включая имя пользователя, электронную почту и пароль.
    Поддерживает фильтрацию и поиск по имени пользователя и электронной почте.
    """
    list_display = (
        'username',
        'pk',
        'email',
        'password',
        'first_name',
        'last_name',
    )
    list_editable = ('password', )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = 'Н/Д'


@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели подписок.
    Позволяет просматривать и редактировать подписки пользователей,
    включая информацию о подписчике и авторе подписки.
    """
    list_display = ('pk', 'user', 'author')
    list_editable = ('user', 'author')
    empty_value_display = 'Н/Д'
