from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = "Создаёт группу 'Модератор продуктов' с нужными правами"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")

        content_type = ContentType.objects.get_for_model(Product)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=["can_unpublish_product", "delete_product"]
        )

        group.permissions.set(permissions)
        group.save()

        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' создана и настроена."))
