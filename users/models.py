from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Класс представления пользователя.
    """

    email = models.EmailField(unique=True)
    phone_number =models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        """
        Возвращает строковое представление поля 'email'.
        """
        return self.email
