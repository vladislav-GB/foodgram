from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from recipes.models import Recipe, Favourite, ShoppingList, RecipeIngredientsRelated, Ingredient
from .serializers import RecipeSerializer, CustomUserSerializer, IngredientSerializer
from users.models import Subscription
import csv

User = get_user_model()

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(
        detail=True, 
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            Favourite.objects.get_or_create(
                user=request.user, 
                recipe=recipe
            )
            return Response(status=status.HTTP_201_CREATED)
        Favourite.objects.filter(
            user=request.user, 
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, 
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            ShoppingList.objects.get_or_create(
                user=request.user, 
                recipe=recipe
            )
            return Response(status=status.HTTP_201_CREATED)
        ShoppingList.objects.filter(
            user=request.user, 
            recipe=recipe
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, 
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredientsRelated.objects.filter(
            recipe__shoppinglist__user=request.user
        ).values(
            'ingredients__name',
            'ingredients__measurement'
        ).annotate(total=Sum('count'))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(['Ингредиент', 'Количество', 'Единица измерения'])
        
        for item in ingredients:
            writer.writerow([
                item['ingredients__name'],
                item['total'],
                item['ingredients__measurement']
            ])

        return response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=True, 
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            Subscription.objects.get_or_create(
                user=request.user, 
                author=author
            )
            return Response(status=status.HTTP_201_CREATED)
        Subscription.objects.filter(
            user=request.user, 
            author=author
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False, 
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            following__user=request.user
        )
        page = self.paginate_queryset(queryset)
        serializer = CustomUserSerializer(
            page, 
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

