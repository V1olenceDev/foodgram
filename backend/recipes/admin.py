from django.contrib import admin
from django.core.exceptions import ValidationError

from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    empty_value_display = 'Н/Д'


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'cooking_time',
        'text',
        'display_tags',
        'image',
        'author',
        'in_favorites',
        'ingredient'
    )
    list_editable = ('name',
                     'cooking_time',
                     'text',
                     'image',
                     'author',
                     'ingredient')
    readonly_fields = ('in_favorites',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = 'Н/Д'

    @admin.display(description='Теги')
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return models.UserFavoriteRecipe.objects.filter(recipe=obj).count()

    def clean(self):
        # Проверка на наличие ингредиентов и изображения
        if not self.ingredients.exists():
            raise ValidationError(
                "Рецепт должен содержать хотя бы один ингредиент.")
        if not self.image:
            raise ValidationError("Рецепт должен иметь изображение.")


@admin.register(models.RecipeIngredientLink)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@admin.register(models.UserFavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(models.UserShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
