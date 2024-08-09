from rest_framework import viewsets
from inventory.models import Supplier, Category, Product, Batch, InventoryTransaction, Order, OrderItem, Procurement, Sales, InventoryReport, AnalyticsData
from .serializers import SupplierSerializer, CategorySerializer, ProductSerializer, BatchSerializer, InventoryTransactionSerializer, OrderSerializer, OrderItemSerializer, ProcurementSerializer, SalesSerializer, InventoryReportSerializer, AnalyticsDataSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransaction.objects.all()
    serializer_class = InventoryTransactionSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class ProcurementViewSet(viewsets.ModelViewSet):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer

class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer

class InventoryReportViewSet(viewsets.ModelViewSet):
    queryset = InventoryReport.objects.all()
    serializer_class = InventoryReportSerializer

class AnalyticsDataViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsData.objects.all()
    serializer_class = AnalyticsDataSerializer