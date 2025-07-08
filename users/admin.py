from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления пользовательской моделью CustomUser
    через интерфейс администратора. Отображает все поля модели.
    """

    exclude = ('password',)
