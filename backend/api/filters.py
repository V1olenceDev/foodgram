from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe, Tag


class RecipeQueryFilter(FilterSet):
    """
    Настроенный фильтр для модели Recipe в Django.
    Позволяет фильтровать рецепты по различным критериям: по тегам, по автору,
    по наличию в избранном и по наличию в списке покупок пользователя.
    """
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                             queryset=Tag.objects.all())
    is_favorited = filters.BooleanFilter(
        method='filter_favorited_recipes')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_recipes_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_favorited_recipes(self, queryset, name, value):
        """
        Фильтр для выборки рецептов, которые отмечены
        как избранные текущим пользователем.
        """
        user = self.request.user
        if value and user.is_authenticated:
            # Получаем ID избранных рецептов пользователя через related_name
            favorited_recipe_ids = user.favorite_recipes.values_list(
                'recipe_id', flat=True)
            # Фильтруем рецепты по этим ID
            return queryset.filter(id__in=favorited_recipe_ids)
        return queryset

    def filter_recipes_in_shopping_cart(self, queryset, name, value):
        """
        Фильтр для выборки рецептов, которые добавлены в
        список покупок текущим пользователем.
        """
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset
