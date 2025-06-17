from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, ContactInfo


def home(request):
    product_list = Product.objects.order_by('-created_at')
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/home.html', {'page_obj': page_obj})


def contacts(request):
    contact = ContactInfo.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')


        # Здесь можно сохранить сообщение в БД или отправить на почту

        messages.success(request, f'Спасибо, {name}, ваше сообщение отправлено!')
        return redirect('contacts')

    return render(request, 'catalog/contacts.html', {'contact': contact})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})
