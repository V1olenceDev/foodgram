from django.db import models

from core import constants, validators
from users.models import User


class Ingredient(models.Model):
    """
    Модель для хранения информации об ингредиентах.
    Содержит название ингредиента и единицу измерения.
    """
    name = models.CharField(
        'Название',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        ),
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        validators=(
            validators.MinMeasurementUnitLenghtValidator(
                constants.MIN_MEASUREMENT_UNIT_LENGHT
            ),
            validators.CyrillicCharRegexValidator()
        ),
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'name',
                    'measurement_unit',
                ],
                name='unique_name_measurement_unit',
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Модель для хранения тегов рецептов.
    Содержит название тега, его цвет в HEX формате и уникальный слаг.
    """
    name = models.CharField(
        'Название',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        unique=True,
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.CyrillicCharRegexValidator(),
        )
    )
    color = models.CharField(
        'Цвет в HEX',
        unique=True,
        max_length=constants.MAX_TAG_COLOR_LENGHT,

    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        unique=True,
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
            validators.LatinCharRegexValidator(),
        )
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
        max_length=constants.MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT,
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
        ),
    )
    text = models.TextField(
        'Описание',
        validators=(
            validators.TwoCharValidator(constants.MIN_TEXT_LENGHT),
        ),
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, мин',
        validators=(
            validators.MinCookingTimeValueValidator(
                constants.MIN_COOKING_TIME
            ),
            validators.MaxCookingTimeValueValidator(
                constants.MAX_COOKING_TIME
            )
        )
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
        related_name='ingredients_in_recipe',
        verbose_name='Ингредиенты'
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


class RecipeIngredientLink(models.Model):
    """
    Промежуточная модель для связи рецептов с ингредиентами.
    Содержит информацию о рецепте, ингредиенте и количестве
    ингредиента в рецепте.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество',
        validators=(
            validators.MinAmountValidator(
                constants.MIN_AMOUNT
            ),
            validators.MaxAmountValidator(
                constants.MAX_AMOUNT
            )
        )
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
        related_name='favorite_user',
        verbose_name='Добавил в избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
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
        related_name='shopping_user',
        verbose_name='Добавил в корзину'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
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
