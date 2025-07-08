from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)

from .forms import ProductForm
from .models import Category, ContactInfo, Product


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Представление для снятия продукта с публикации.
    Доступно только авторизованным пользователям с соответствующим правом.
    """
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        return redirect('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления продукта.
    Разрешено владельцу продукта или пользователю с правом 'delete_product'.
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')
    permission_required = 'catalog.delete_product'

    def has_permission(self):
        product = self.get_object()
        return (
            self.request.user == product.owner
            or self.request.user.has_perm('catalog.delete_product')
        )


class HomeView(ListView):
    """
    Главная страница с постраничным списком продуктов.
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 6
    ordering = ["-created_at"]


class ContactView(TemplateView):
    """
    Контактная страница и обработка формы обратной связи.
    """

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        """
        Добавляет контактные данные из модели ContactInfo.
        """
        context = super().get_context_data(**kwargs)
        context["contact"] = ContactInfo.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает отправку формы обратной связи и
        выводит сообщение об успешной отправке.
        """
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Здесь можно сохранить сообщение в БД или отправить на почту

        messages.success(request, f"Спасибо, {name}, ваше сообщение отправлено!")
        return self.get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    """
    Страница с подробной информацией о продукте.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Создание нового продукта.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование существующего продукты.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")


class ProductListView(ListView):
    """
    Список всех продуктов.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_list.html"


class CatalogView(View):
    """
    Каталог категорий товаров.
    """

    def get(self, request):
        """
        Вывод всех категорий.
        """
        categories = Category.objects.all()
        return render(request, "catalog/catalog.html", {"categories": categories})


class CategoryProductsView(View):
    """
    Список продуктов в выбранной категории.
    """

    def get(self, request, category_id):
        """
        Выводит все продукты, относящиеся к данной категории.
        """
        category = get_object_or_404(Category, id=category_id)
        products = category.products.order_by("-created_at")
        return render(
            request,
            "catalog/category_products.html",
            {"category": category, "products": products},
        )
