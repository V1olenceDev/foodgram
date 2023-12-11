from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.settings import FILE_NAME
from recipes.models import (
    UserFavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredientLink,
    UserShoppingCart,
    Tag)
from rest_framework import (
    filters,
    mixins,
    status,
    viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import Subscribe, User

from .filters import RecipeQueryFilter
from .pagination import RecipePageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    UserSubscriptionsSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeDetailReadSerializer,
    RecipeSerializer,
    AuthorSubscriptionSerializer,
    TagSerializer)


class UserProfileViewSet(viewsets.GenericViewSet):
    """
    Вьюсет для управления профилями пользователей.
    Поддерживает создание,
    просмотр списка и детальный просмотр профилей.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = RecipePageNumberPagination

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,),
            pagination_class=RecipePageNumberPagination)
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = UserSubscriptionsSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs['pk'])

        if request.method == 'POST':
            serializer = AuthorSubscriptionSerializer(
                author, data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=request.user, author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Subscribe, user=request.user,
                              author=author).delete()
            return Response({'detail': 'Успешно'},
                            status=status.HTTP_204_NO_CONTENT)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    Вьюсет для управления кулинарными тегами.
    Позволяет получить список всех тегов
    и детальную информацию о каждом теге.
    """
    permission_classes = (AllowAny, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class FoodIngredientViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """
    Вьюсет для управления ингредиентами блюд.
    Поддерживает получение списка
    и детальной информации об ингредиентах.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', )


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления кулинарными рецептами.
    Поддерживает все основные
    операции CRUD для рецептов.
    """
    queryset = Recipe.objects.all()
    pagination_class = RecipePageNumberPagination
    permission_classes = (IsAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeQueryFilter
    http_method_names = ['get', 'post', 'patch', 'create', 'delete']

    def get_serializer_class(self):
        """
        Определяет класс сериализатора в зависимости от действия.
        """
        if self.action in ('list', 'retrieve'):
            return RecipeDetailReadSerializer
        return RecipeCreateSerializer

    def handle_action(self, model_class, request, recipe_id, response_message):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            if not model_class.objects.filter(user=request.user,
                                              recipe=recipe).exists():
                model_class.objects.create(user=request.user, recipe=recipe)
                serializer = RecipeSerializer(recipe,
                                              context={"request": request})
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'errors': 'Элемент уже добавлен.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            get_object_or_404(model_class, user=request.user,
                              recipe=recipe).delete()
            return Response({'detail': response_message},
                            status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, **kwargs):
        return self.handle_action(UserFavoriteRecipe,
                                  request,
                                  kwargs['pk'], 'Рецепт удален из избранного.')

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        return self.handle_action(UserShoppingCart,
                                  request,
                                  kwargs['pk'],
                                  'Рецепт удален из списка покупок.')

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (
            RecipeIngredientLink.objects
            .filter(recipe__usershoppingcart__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list('ingredient__name', 'total_amount',
                         'ingredient__measurement_unit')
        )
        file_list = []
        [file_list.append(
            '{} - {} {}.'.format(*ingredient)) for ingredient in ingredients]
        file = HttpResponse('Cписок покупок:\n' + '\n'.join(file_list),
                            content_type='text/plain')
        file['Content-Disposition'] = (f'attachment; filename={FILE_NAME}')
        return file
