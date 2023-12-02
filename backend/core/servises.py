from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers import RecipeSerializer
from recipes.models import Recipe


def creation_favorite_or_shopping_cart_recipe(model, user, id):
    recipe = get_object_or_404(Recipe, id=id)
    if model.objects.filter(user=user, recipe=recipe).exists():
        return Response(
            {"errors": "Вы уже добавили этот рецепт!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    model.objects.create(user=user, recipe=recipe)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_recipe_from_favorite_or_shopping_cart(model, user, id):
    favorite_or_in_shopping_cart_recipe = model.objects.filter(
        user=user, recipe__id=id
    )
    if favorite_or_in_shopping_cart_recipe.exists():
        favorite_or_in_shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"errors": "Вы уже удалили этот рецепт!"},
        status=status.HTTP_400_BAD_REQUEST,
    )