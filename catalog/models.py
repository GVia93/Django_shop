from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Категория товара.
    Хранит информацию о наименовании и описании категории.
    """

    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """
        Возвращает строковое представление категории.
        """
        return self.name


class Product(models.Model):
    """
    Продукт каталога.

    Содержит сведения о товаре: название, описание, изображение, категория,
    цена, дата создания и последнего обновления.
    """

    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/", null=True, blank=True, verbose_name="Изображение"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта'),
        ]

    def __str__(self):
        """
        Возвращает строковое представление продукта.
        """
        return self.name


class ContactInfo(models.Model):
    """
    Контактная информация компании или продавца.
    Содержит адрес, телефон и email.
    """

    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        """
        Возвращает строковое представление контактной информации.
        """
        return f"{self.address} | {self.phone}"
