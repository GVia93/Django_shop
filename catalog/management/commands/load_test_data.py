from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет все данные и загружает тестовые категории и продукты'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        vegetables = Category.objects.create(name='Овощи', description='Свежие овощи')
        fruits = Category.objects.create(name='Фрукты', description='Сочные фрукты')

        Product.objects.create(name='Огурец', price=15.0, category=vegetables)
        Product.objects.create(name='Помидор', price=20.0, category=vegetables)
        Product.objects.create(name='Яблоко', price=25.0, category=fruits)

        self.stdout.write(self.style.SUCCESS('Тестовые данные загружены.'))
