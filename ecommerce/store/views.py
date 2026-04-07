from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product,Cart,CartItem
from .serializers import ProductSerializer, AddtoCartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
class CreateCartAPIView(APIView):
    def post(self,request):
        cart=Cart.objects.create()
        return Response({"cart_id": cart.id})

class AddToCartAPIView(APIView):
    def post(self,request,cart_id):
        serializer=AddtoCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)
        
        try:
            cart=Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({'error':'Cart not found'},status=404)
        


        product_id=serializer.validated_data['product_id']
        quantity=serializer.validated_data['quantity']

        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error':'Product not found'},status=404)
        
        cart_item,created=CartItem.objects.get_or_create(
            cart_id=cart_id,
            product=product,
            defaults={'quantity': quantity }
        )

        if not created:
            cart_item.quantity+=quantity
            cart_item.save()
                                        
        return Response({"message":"Object added successfully"})
    
class RemoveFromCartAPIView(APIView):

    def delete(self,request,cart_id,product_id):

        try:
            cart_item=CartItem.objects.get(
                cart_id=cart_id,
                product_id=product_id
            )
            cart_item.delete()
            return Response({"message":"Item removed successfully"})
        except CartItem.DoesNotExist:
            return Response({"error":"not found"},status=404)

class ViewCartAPIView(APIView):
    def get(self,request,cart_id):
        items=CartItem.objects.filter(
            cart_id=cart_id
        ).select_related('product')
        data=[]

        for i in items:
            data.append({
                'product':i.product.name,
                'price': i.product.price,
                'quantity':i.quantity
            })
        return Response(data)
    
        