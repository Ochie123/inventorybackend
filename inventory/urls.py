from django.urls import path
from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('scan-product/', views.scan_product, name='scan_product'),
    path('products/<str:sku>/', views.get_product_by_sku, name='get_product_by_sku'),
]