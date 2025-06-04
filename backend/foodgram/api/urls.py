from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),                   # /api/users/, /api/recipes/ и т.д.
    path('auth/', include('djoser.urls')),            # /auth/users/, /auth/users/me/
    path('auth/', include('djoser.urls.authtoken')),  # /auth/token/login/, /auth/token/logout/
]
