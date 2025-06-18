from django.contrib import messages
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView, DetailView
from .models import Product, ContactInfo, Category


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6
    ordering = ['-created_at']


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = ContactInfo.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        name =request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Здесь можно сохранить сообщение в БД или отправить на почту

        messages.success(request, f'Спасибо, {name}, ваше сообщение отправлено!')
        return self.get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class CatalogView(View):

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'catalog/catalog.html', {'categories': categories})


class CategoryProductsView(View):

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        products = category.products.order_by('-created_at')
        return render(request, 'catalog/category_products.html', {
            'category': category,
            'products': products
        })
