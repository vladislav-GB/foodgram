from django.urls import path, include
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.routers import SimpleRouter
from . import views

router = DefaultRouter()
router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('users', views.UserViewSet, basename='users')

auth_router = SimpleRouter()
auth_router.register('users', DjoserUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),           
    path('auth/', include('djoser.urls.authtoken')), 
]