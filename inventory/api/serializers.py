from rest_framework import serializers
from inventory.models import Supplier, Category, Product, Batch, InventoryTransaction, Order, OrderItem, Procurement, Sales, InventoryReport, AnalyticsData

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'description', 
            'category', 
            'sku', 
            'barcode', 
            'quantity', 
            'reorder_level', 
            'qr_code', 
            'buying_price', 
            'selling_price',
            'manufacture_date',
            'expiry_date',
        ]


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'

class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    product_names = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'fulfilled', 'customer', 'customer_name', 'products', 'product_names']

    def get_product_names(self, obj):
        return [product.name for product in obj.products.all()]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'order', 'product']

class ProcurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procurement
        fields = '__all__'

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class InventoryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryReport
        fields = '__all__'

class AnalyticsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsData
        fields = '__all__'