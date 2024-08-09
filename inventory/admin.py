from django.contrib import admin
from .models import Supplier, Category, Product, Batch, InventoryTransaction, Order, OrderItem, Procurement, Sales, InventoryReport, AnalyticsData

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'barcode', 'quantity', 'reorder_level', 'buying_price', 'selling_price')
    search_fields = ['name', 'sku']
    list_filter = ('category',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('product', 'batch_number', 'quantity', 'manufacturing_date', 'expiry_date', 'created_at')
    search_fields = ('batch_number', 'product__name')
    list_filter = ('product', 'manufacturing_date', 'expiry_date')

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'batch', 'quantity', 'transaction_type', 'timestamp')
    search_fields = ('product__name', 'batch__batch_number')
    list_filter = ('transaction_type', 'timestamp')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at', 'fulfilled')
    search_fields = ('customer__username',)
    list_filter = ('created_at', 'fulfilled')
    inlines = [OrderItemInline]

@admin.register(Procurement)
class ProcurementAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'order_date', 'delivery_date', 'quantity_ordered')
    search_fields = ('product__name', 'supplier__name')
    list_filter = ('order_date', 'delivery_date')

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'sales_date')
    search_fields = ('product__name', 'customer__username')
    list_filter = ('sales_date',)

@admin.register(InventoryReport)
class InventoryReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'total_products', 'total_quantity')
    search_fields = ('report_date',)
    list_filter = ('report_date',)

@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ('date', 'product', 'sales_quantity', 'sales_value', 'stock_level')
    search_fields = ('product__name', 'date')
    list_filter = ('date', 'product')