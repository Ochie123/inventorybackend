from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views

#router = routers.DefaultRouter()
router = DefaultRouter()
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'batches', views.BatchViewSet)
router.register(r'inventory-transactions', views.InventoryTransactionViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'procurements', views.ProcurementViewSet)
router.register(r'sales', views.SalesViewSet)
router.register(r'inventory-reports', views.InventoryReportViewSet)
router.register(r'analytics-data', views.AnalyticsDataViewSet)

app_name = 'inventory'
urlpatterns = [
    path('', include(router.urls)),
    # ... your other URL patterns ...
]