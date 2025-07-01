from django.urls import path
from .views import ContactView, ProductDetailView, HomeView, CatalogView, CategoryProductsView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('catalog/category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
]
