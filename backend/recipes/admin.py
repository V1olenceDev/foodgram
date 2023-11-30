from django.contrib import admin

from . import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Ingredient.
    Предоставляет возможность отображения, фильтрации и поиска по ингредиентам.
    """
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Tag.
    Позволяет редактировать и просматривать теги, включая их название,
    цвет и слаг.
    """
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    empty_value_display = 'Н/Д'


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Recipe.
    Позволяет отображать, редактировать и фильтровать рецепты.
    Включает дополнительные поля для отображения тегов и
    количества добавлений в избранное.
    """
    list_display = (
        'pk',
        'name',
        'cooking_time',
        'text',
        'display_tags',
        'image',
        'author',
        'in_favorites'
    )
    list_editable = ('name', 'cooking_time', 'text', 'image', 'author')
    readonly_fields = ('in_favorites',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = 'Н/Д'

    @admin.display(description='Теги')
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorite_recipe.count()


@admin.register(models.Recipe_ingredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели RecipeIngredientLink
    (ранее Recipe_ingredient).
    Предоставляет возможности для управления связями
    между рецептами и ингредиентами.
    """
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели UserFavoriteRecipe (ранее Favorite).
    Позволяет управлять избранными рецептами пользователей.
    """
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(models.Shopping_cart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели UserShoppingCart
    (ранее Shopping_cart).
    Позволяет управлять списком покупок пользователей,
    включая добавление и удаление рецептов.
    """
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
