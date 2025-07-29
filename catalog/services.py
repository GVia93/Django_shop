from .models import Product


def get_products_by_category_id(category_id):
    """
    Возвращает список опубликованных продуктов для указанной категории по ID.
    """

    return Product.objects.filter(category_id=category_id, is_published=True)
