from django.contrib.auth.models import AbstractUser
from django.db import models

from core import constants, validators


class User(AbstractUser):
    """
    Пользовательская модель, расширяющая стандартную
    модель пользователя Django.
    Включает стандартные поля пользователя
    Django и добавляет уникальное поле email.
    """
    email = models.EmailField(
        verbose_name='Email',
        max_length=constants.MAX_EMAEL_LENGHT,
        unique=True,
        help_text='Введите адрес электронной почты.',
    )
    username = models.CharField(
        verbose_name='Ник',
        max_length=254,
        unique=True,
        help_text='Введите ник пользователя',
        validators=(
            validators.validate_username,
            validators.LatinCharRegexValidator(),
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
        )
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=constants.MAX_USER_LENGHT,
        help_text='Введите свое имя',
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        )
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=constants.MAX_USER_LENGHT,
        help_text='Введите свою фамилию',
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        )
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=constants.MAX_USER_LENGHT,
        help_text='Введите свой пароль'

    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'username',
                    'email',
                ],
                name='unique_username_email',
            ),
        )

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """
    Модель для хранения информации о подписках пользователей.
    Содержит ссылки на подписчика (user) и автора (author),
    на которого он подписан.
    Устанавливает ограничение на уникальность комбинации
    подписчика и автора.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Подписан'
    )
    subscription_date = models.DateTimeField(
        verbose_name='Дата подписки',
        auto_now=True,
    )

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'

    class Meta:
        ordering = ('subscription_date',)
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            ),
            models.CheckConstraint(
                check=~models.Q(user_id=models.F('author_id')),
                name='no_self_subscription'
            ),
        )
