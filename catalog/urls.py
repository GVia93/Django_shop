from django.urls import path

from . import views
from .views import (CatalogView, CategoryProductsView, ContactView, HomeView,
                    ProductCreateView, ProductDetailView, ProductListView, ProductUnpublishView, ProductPublishView)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("catalog/category/<int:category_id>/", CategoryProductsView.as_view(), name="category_products"),
]

urlpatterns += [
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product_create/", ProductCreateView.as_view(), name="product_create"),
    path("product_list/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('product/<int:pk>/publish/', ProductPublishView.as_view(), name='product_publish'),
]
