from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView, View)

from .forms import ProductForm
from .models import Category, ContactInfo, Product
from .services import get_products_by_category_id


class ProductPublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Представление для публикации продукта.
    Доступно только авторизованным пользователям с соответствующим правом.
    """

    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = True
        product.save(update_fields=["is_published"])
        return redirect("catalog:product_list")


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Представление для снятия продукта с публикации.
    Доступно только авторизованным пользователям с соответствующим правом.
    """

    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save(update_fields=["is_published"])
        return redirect("catalog:product_list")


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Представление для удаления продукта.
    Разрешено владельцу продукта или пользователю с правом 'delete_product'.
    """

    model = Product
    success_url = reverse_lazy("catalog:product_list")
    permission_required = "catalog.delete_product"

    def has_permission(self):
        """
        Проверяет, имеет ли пользователь право удалить продукт.
        Доступ разрешён владельцу продукта или пользователю с правом 'catalog.delete_product'.
        """
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm(
            "catalog.delete_product"
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

    def get_queryset(self):
        """
        Возвращает QuerySet с опубликованными продуктами.
        Фильтрует объекты модели Product, чтобы отображались только те,
        у которых флаг is_published установлен в True.
        """
        return Product.objects.filter(is_published=True)


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


@method_decorator(cache_page(60 * 15), name="dispatch")
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
    Представление для создания нового продукта.
    Доступно только авторизованным пользователям.
    Поле 'owner' автоматически заполняется текущим пользователем.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """
        Устанавливает текущего пользователя как владельца продукта
        перед сохранением формы.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Представление для редактирования продукта.
    Доступно только владельцу продукта.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        """
        Проверяет, является ли текущий пользователь владельцем объекта.
        Используется для ограничения доступа к редактированию или удалению.
        """
        return self.request.user == self.get_object().owner


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


class CategoryProductListView(ListView):
    """
    Представление для отображения списка опубликованных продуктов,
    принадлежащих определённой категории.
    """

    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        """
        Возвращает QuerySet продуктов, отфильтрованных по категории и опубликованному статусу.
        """
        return get_products_by_category_id(self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """
        Добавляет объект категории в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(id=self.kwargs.get("pk"))
        return context

