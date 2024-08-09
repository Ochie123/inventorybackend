from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import InventoryTransaction, Product, OrderItem, Order, Sales
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def scan_product(request):
    if request.method == 'GET':
        # Render the HTML template for GET requests
        return render(request, 'product.html')
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        sku = data.get('sku')
        action = data.get('action')  # 'add_to_basket' or 'sell'
        quantity = data.get('quantity', 1)

        product = get_object_or_404(Product, sku=sku)

        if action == 'add_to_basket':
            # Handle adding to basket for any user
            order, created = Order.objects.get_or_create(
                customer=request.user if request.user.is_authenticated else None,
                fulfilled=False
            )

            # Add the product to the order
            order_item, created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                order_item.quantity += quantity
                order_item.save()

            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} added to basket',
                'quantity': order_item.quantity
            })

        elif action == 'sell':
            # Ensure only authenticated users can sell
            if not request.user.is_authenticated:
                return JsonResponse({'status': 'error', 'message': 'User not authenticated for selling'}, status=403)

            # Create a new Sales object
            sale = Sales.objects.create(
                product=product,
                customer=request.user,
                quantity=quantity
            )

            # Update product quantity
            product.quantity -= quantity
            product.save()

            # Create an InventoryTransaction
            InventoryTransaction.objects.create(
                product=product,
                quantity=quantity,
                transaction_type=InventoryTransaction.OUT
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{product.name} sold',
                'quantity': quantity
            })

        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid action'
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def get_product_by_sku(request, sku):
    product = get_object_or_404(Product, sku=sku)
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'sku': product.sku,
        'quantity': product.quantity,
        'selling_price': product.selling_price,
    })
