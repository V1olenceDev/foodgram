from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from recipes.constants import (
    MAX_LENGTH_NAME,
    MAX_LENGTH_MEASUREMENT_UNIT,
    MAX_LENGTH_SLUG,
    MAX_LENGTH_COLOR)
from users.models import User


class Ingredient(models.Model):
    """
    Модель для хранения информации об ингредиентах.
    Содержит название ингредиента и единицу измерения.
    """
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_NAME,
        validators=[
            RegexValidator(
                regex='^#([a-fA-F0-9]{3,6})$',
                message='Название должно содержать только буквы, '
                'цифры и пробелы.'
            )
        ]
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAX_LENGTH_MEASUREMENT_UNIT
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient_name_measurement')
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Модель для хранения тегов рецептов.
    Содержит название тега, его цвет в HEX формате и уникальный слаг.
    """
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_NAME
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=MAX_LENGTH_COLOR,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{3,6})$',  # Упрощенное регулярное выражение
                message='Поле должно содержать HEX-код выбранного цвета.'
            )
        ]
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=MAX_LENGTH_SLUG,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(fields=['name', 'color'],
                                    name='unique_name_color')
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Основная модель для хранения рецептов.
    Содержит информацию о названии, описании,
    времени приготовления, изображении,
    дате публикации, авторе и связанных тегах и ингредиентах.
    """
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH_NAME
    )
    text = models.TextField(
        'Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, мин',
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientLink',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты в рецепте'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_detailed_ingredients(self):
        """
        Возвращает список ингредиентов с количеством для этого рецепта.
        """
        ingredients_with_amounts = self.ingredients.select_related(
            'ingredient').all()
        return [
            {
                'ingredient': link.ingredient.name,
                'amount': link.amount,
                'measurement_unit': link.ingredient.measurement_unit
            }
            for link in ingredients_with_amounts
        ]


class RecipeIngredientLink(models.Model):
    """
    Промежуточная модель для связи рецептов с ингредиентами.
    Содержит информацию о рецепте, ингредиенте и количестве
    ингредиента в рецепте.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_combination'
            )
        ]

    def __str__(self):
        return (f'{self.recipe.name}: '
                f'{self.ingredient.name} - '
                f'{self.amount} '
                f'{self.ingredient.measurement_unit}')


class UserFavoriteRecipe(models.Model):
    """
    Модель для хранения информации об избранных рецептах пользователей.
    Содержит ссылки на пользователя и избранный рецепт.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class UserShoppingCart(models.Model):
    """
    Модель для хранения информации о рецептах в корзине покупок пользователя.
    Содержит ссылки на пользователя и рецепт, добавленный в корзину.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в корзине'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
