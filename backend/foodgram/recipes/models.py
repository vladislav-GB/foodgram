from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Обязательно, не более 200 символов',
    )
    measurement = models.CharField(
        'Единица измерения',
        max_length=200,
        help_text='Обязательно, укажите единицу измерения',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement'),
                name='unique_name_measurement'
            )
        ]


class Recipe(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Обязательное, не более 200 символов',
    )
    image = models.ImageField(
        '',
        upload_to='recipes/images',
        help_text='Обязательно, добавьте изображение рецепта'
    )
    text = models.TextField(
        'Описание',
        help_text='Обязательно, опишите последовательность приготовления'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientsRelated',
        verbose_name='',
        help_text='Обязательно, укажите ингредиенты',
    )
    time_cooking = models.IntegerField(
        'Время приготовления',
        help_text='Обязательно, укажите время в минутах',
        validators=(MaxValueValidator(180), MinValueValidator(15)),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class RecipeIngredientsRelated(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredints',
        verbose_name='рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredints',
        verbose_name='ингредиент'
    )
    count = models.IntegerField(
    validators=(MinValueValidator(1), MaxValueValidator(1000)),
)

    class Meta:
        verbose_name = 'связь рецептов и ингридиентов'
        verbose_name_plural = 'связи рецептов и ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredients'),
                name='constraints'
            ),
        ]


class AbstractUserRecipeModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_recipe',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='user_recipe',
        verbose_name='рецепт'
    )

    class Meta:
        abstract = True


class ShoppingList(AbstractUserRecipeModel):

    class Meta:
        verbose_name = 'покупки'
        verbose_name_plural = 'покупки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shooping_list'
            )
        ]


class Favourite(AbstractUserRecipeModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourites',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favourite'
            )
        ]
