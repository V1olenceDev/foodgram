from django.contrib import admin
from django import forms
from .models import (Ingredient,
                     Tag,
                     Recipe,
                     UserFavoriteRecipe,
                     UserShoppingCart,
                     RecipeIngredientLink)


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")

        if not image:
            self.add_error(
                'image',
                'Необходимо добавить изображение для рецепта.')

        return cleaned_data


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredientLink
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    inlines = [RecipeIngredientInline]
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
        return UserFavoriteRecipe.objects.filter(recipe=obj).count()

    def save_formset(self, request, form, formset, change):
        if formset.model != RecipeIngredientLink:
            return super().save_formset(request, form, formset, change)

        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.ingredient:
                formset.add_error(
                    None,
                    'Необходимо добавить хотя бы один ингредиент.')
            instance.save()
        formset.save_m2m()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    empty_value_display = 'Н/Д'


@admin.register(UserFavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')


@admin.register(UserShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
