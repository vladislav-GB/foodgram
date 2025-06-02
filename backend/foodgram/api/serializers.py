from rest_framework import serializers
from users.models import User
from recipes.models import (
    Recipe, RecipeIngredientsRelated, Ingredient, ShoppingList, Favourite)

class IngredientSerializer(serializers.ModelSerializer):
    # for ingredients

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientsRelatedSerializer(serializers.ModelSerializer):
    # for ingredients in recipe
    class Meta:
        model = RecipeIngredientsRelated
        fields = ('recipe', 'ingredients', 'count')


class RecipeSerializer(serializers.ModelSerializer):
    # for recipes

    class Meta:
        model = Recipe
        fields = '__all__'


class ShoppingListSerializer(serializers.ModelSerializer):
    # for shoppng list
    class Meta:
        model = ShoppingList
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    # for favourite recipes
    class Meta:
        model = Favourite
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # for users
    class Meta:
        model = User
        fields = '__all__'

# serializer for base64 images decoder!