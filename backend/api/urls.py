from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('tags', views.TagViewSet, basename='tags')
router.register('users', views.UserProfileViewSet, basename='users')
router.register('ingredients', views.FoodIngredientViewSet,
                basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
