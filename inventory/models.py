from datetime import date
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
import uuid
from barcode import Code128
from barcode.writer import ImageWriter

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # Not mandatory
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    barcode = models.ImageField(upload_to='barcodes', blank=True)  # Changed to ImageField
    quantity = models.IntegerField()
    reorder_level = models.IntegerField()
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    manufacture_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)  # New field to track if the product is expired

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate SKU if not provided
        if not self.sku:
            self.sku = uuid.uuid4().hex[:6]  # Generate a 6-character unique identifier
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.sku)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer)
        self.qr_code.save(f'{self.sku}.png', File(buffer), save=False)
        
        # Generate Barcode
        barcode_img = Code128(self.sku, writer=ImageWriter())
        buffer = BytesIO()
        barcode_img.write(buffer)
        self.barcode.save(f'{self.sku}.png', File(buffer), save=False)
        
        # Check if the product is expired
        if self.expiry_date and self.expiry_date < date.today():
            self.is_expired = True
        else:
            self.is_expired = False
        
        super().save(*args, **kwargs)

class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=100)
    quantity = models.IntegerField()
    manufacturing_date = models.DateField(null=True, blank=True)  # Not mandatory
    expiry_date = models.DateField(null=True, blank=True)  # Not mandatory
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.product.name} - {self.batch_number}'

class InventoryTransaction(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    TRANSACTION_TYPE_CHOICES = [
        (IN, 'In'),
        (OUT, 'Out'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)  # Not mandatory
    quantity = models.IntegerField()
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.transaction_type} - {self.product.name} - {self.quantity}'

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null and blank values
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(default=timezone.now)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        if self.customer:
            return f'Order #{self.id} - {self.customer.username}'
        return f'Order #{self.id} - Anonymous'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
class Procurement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True, blank=True)  # Not mandatory
    quantity_ordered = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} from {self.supplier.name}'

class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    sales_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.product.name}'

class InventoryReport(models.Model):
    report_date = models.DateTimeField(default=timezone.now)
    total_products = models.IntegerField()
    total_quantity = models.IntegerField()

    def __str__(self):
        return f'Report for {self.report_date}'

class AnalyticsData(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sales_quantity = models.IntegerField(default=0)
    sales_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_level = models.IntegerField(default=0)

    class Meta:
        unique_together = ('date', 'product')

    def __str__(self):
        return f"{self.product.name} - {self.date}"