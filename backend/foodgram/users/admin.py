from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import Group
from users.models import User


class CustomUserAdmin(UserAdmin):
    'Интерфейс админ-зоны'

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',)
    search_fields = ('userfield', 'email')


admin.site.register(User, CustomUserAdmin)