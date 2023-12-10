from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser

from users.constants import (
    MAX_EMAIL_LENGTH,
    MAX_LENGTH_NAME)
from users.validators import regex_name_validator


class User(AbstractUser):
    """Пользовательская модель, расширяющая
    стандартную модель пользователя Django."""
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH, unique=True)
    first_name = models.CharField('Имя',
                                  max_length=MAX_LENGTH_NAME,
                                  validators=[regex_name_validator])
    last_name = models.CharField('Фамилия',
                                 max_length=MAX_LENGTH_NAME,
                                 validators=[regex_name_validator])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """ Модель для хранения информации о подписках пользователей. """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscribers',
                             verbose_name='Подписчик')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='subscribing',
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_subscribe'),
            models.CheckConstraint(check=~Q(user=models.F('author')),
                                   name='prevent_self_subscribe')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
