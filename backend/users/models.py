from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CheckConstraint, Q
from django.contrib.auth.models import AbstractUser

from users.constants import MAX_EMAIL_LENGTH

# Валидаторы для имени и фамилии
name_validator = RegexValidator(r'^[A-Za-zА-Яа-я\s]+$',
                                'Только буквы и пробелы разрешены.')


class User(AbstractUser):
    """Пользовательская модель, расширяющая
    стандартную модель пользователя Django."""
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH, unique=True)
    first_name = models.CharField('Имя',
                                  max_length=150,
                                  blank=False,
                                  validators=[name_validator])
    last_name = models.CharField('Фамилия',
                                 max_length=150,
                                 blank=False,
                                 validators=[name_validator])

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
            CheckConstraint(check=~Q(user=models.F('author')),
                            name='prevent_self_subscribe')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
