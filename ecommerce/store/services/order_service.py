from django.db import transaction
from ..models import Cart,CartItem,Order,OrderItem
from rest_framework.response import Response
def place_order(cart_id):
        
        try:                
                cart=Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
                return Response({'message':'Cart not found'},status=404)
            
        cart_items=CartItem.objects.filter(cart=cart).select_related('product')
        if not cart_items.exists():
            return Response({"message":"Cart is empty"},status=400)

        with transaction.atomic():
                

                for i in cart_items:
                    if i.product.stock<i.quantity:
                        return Response({"message":f"Out of stockfor {i.product.name}"},status=400)

                    order= Order.objects.create()

                    for i in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=i.product,
                            quantity=i.quantity
                        )

                        i.product.stock-=i.quantity
                        i.product.save()

                    cart_items.delete()
        return Response({"message":'Order placed successfully',"order_id": order.id},status=200)