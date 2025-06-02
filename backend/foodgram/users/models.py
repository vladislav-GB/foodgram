from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=200,
        unique=True,
        help_text='обязательное, не более 200 символов',
        validators=[UnicodeUsernameValidator()],
        error_messages={'unique': 'Пользователь с таким именем уже существует.'}
    )
    email = models.EmailField(
        'Почта',
        max_length=200,
        unique=True,
        help_text='обязательное, не более 200 символов',
    )
    first_name = models.CharField(
        'Имя',
        max_length=200,
        help_text='обязательное, не более 200 символов',
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=200,
        help_text='обязательное, не более 200 символов',
    )
    password = models.CharField(
        'Пароль',
        max_length=20,
        help_text='обязательное, от 8 до 20 символов',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'пользователь'
        ordering = ('username',)
        db_table = 'users_user'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    'Модель для подписок',
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Пользователь',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'подписка'
        constraints = [
            models.UniqueConstraint(
                fields=('subscription', 'following'),
                name='unique_name_following'
            )
        ]
