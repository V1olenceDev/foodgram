from django.db import transaction
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (
    UserFavoriteRecipe,
    UserShoppingCart,
    Ingredient,
    Recipe,
    RecipeIngredientLink,
    Tag)
from users.models import Subscribe, User


class UserProfileReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения информации о пользователе.
    Определяет, подписан ли текущий пользователь на автора.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and user.subscribing.filter(
            author=obj).exists()


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления краткой информации о рецепте.
    Используется для представления рецептов в списках подписок и избранного.
    """
    image = Base64ImageField(read_only=True)
    name = serializers.ReadOnlyField()
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Recipe
        fields = ('id', 'name',
                  'image', 'cooking_time')


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления подписок пользователя.
    Включает информацию о подписанных авторах и их рецептах.
    """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Subscribe.objects.filter(user=self.context['request'].user,
                                         author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            try:
                recipes = recipes[:int(limit)]
            except ValueError:
                return serializers.ValidationError("Неверное значение.")
        return RecipeSerializer(recipes, many=True, read_only=True).data


class AuthorSubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписки на авторов рецептов.
    Включает информацию о авторе и его рецептах.
    """
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def validate(self, obj):
        if (self.context['request'].user == obj):
            raise serializers.ValidationError(
                {'errors': 'Невозможно подписаться.'})
        return obj

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Subscribe.objects.filter(user=self.context['request'].user,
                                         author=obj).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления информации об ингредиентах блюд.
    """
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для представления кулинарных тегов.
    """
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального представления ингредиентов в рецепте.
    Включает информацию об ингредиенте и его количестве.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredientLink
        fields = ('id', 'name',
                  'measurement_unit', 'amount')


class RecipeDetailReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального чтения рецепта.
    Включает автора, теги, ингредиенты, и
    информацию об избранном и списке покупок.
    """
    author = UserProfileReadSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientDetailSerializer(
        many=True, read_only=True, source='recipes')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image',
                  'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and UserFavoriteRecipe.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and UserShoppingCart.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        )


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания ингредиентов рецепта.
    Используется в процессе создания или обновления рецепта для обработки
    информации об ингредиентах, включая их идентификаторы и количества.
    """
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredientLink
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления рецептов.
    Обрабатывает информацию о рецепте, включая ингредиенты, теги, изображение,
    название, описание и время приготовления.
    Также обеспечивает валидацию данных.
    Поддерживает транзакционное добавление тегов и ингредиентов.
    """
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    author = UserProfileReadSerializer(read_only=True)
    id = serializers.ReadOnlyField()
    ingredients = RecipeIngredientCreateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients',
                  'tags', 'image',
                  'name', 'text',
                  'cooking_time', 'author')

    def validate(self, obj):
        for field in ['name', 'text', 'cooking_time']:
            if not obj.get(field):
                raise serializers.ValidationError(
                    f'{field} - Обязательное поле.'
                )
        if not obj.get('tags'):
            raise serializers.ValidationError(
                'Нужно указать минимум 1 тег.'
            )
        if not obj.get('ingredients'):
            raise serializers.ValidationError(
                'Нужно указать минимум 1 ингредиент.'
            )
        inrgedient_id_list = [item['id'] for item in obj.get('ingredients')]
        unique_ingredient_id_list = set(inrgedient_id_list)
        if len(inrgedient_id_list) != len(unique_ingredient_id_list):
            raise serializers.ValidationError(
                'Ингредиенты должны быть уникальны.'
            )
        return obj

    @transaction.atomic
    def tags_and_ingredients_set(self, recipe, tags, ingredients):
        recipe.tags.set(tags)
        RecipeIngredientLink.objects.bulk_create(
            [RecipeIngredientLink(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        self.tags_and_ingredients_set(recipe, tags, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)

        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        if tags:
            instance.tags.set(tags)

        if ingredients:
            RecipeIngredientLink.objects.filter(recipe=instance).delete()
            ingredient_links = [
                RecipeIngredientLink(
                    recipe=instance,
                    ingredient_id=ingredient['id'],
                    amount=ingredient['amount']
                )
                for ingredient in ingredients
            ]
            RecipeIngredientLink.objects.bulk_create(ingredient_links)

        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeDetailReadSerializer(
            instance, context=self.context).data
