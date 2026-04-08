from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product,Cart,CartItem,Order,OrderItem
from .serializers import ProductSerializer, AddtoCartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .services.order_service import place_order

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
        if quantity>=product.stock:
            return Response({'error':'Insufficient stock'},status=400)
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
        if not Cart.objects.filter(id=cart_id).exists():
            return Response({'error':'Cart not found'},status=404)
        items=CartItem.objects.filter(
            cart_id=cart_id
        ).select_related('product')


        data=[]
        total=0
        for i in items:
            data.append({
                'product':i.product.name,
                'price': i.product.price,
                'quantity':i.quantity,
                'total':i.product.price*i.quantity
            })
        
            total+=i.product.price*i.quantity
        return Response({"items":data,"cart_total":total})
    

class PlaceOrderAPIView(APIView):
    def post(self,request,cart_id):
        data,status_code=place_order(cart_id)
        return Response(data,status=status_code)
class UpdateProductAPIView(APIView):
    def put(self,request,product_id):
        try:
            product=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error':'Product not found'},status=404)

        serializer=ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
                


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def get_queryset(self):
        
        queryset=super().get_queryset()
        search=self.request.query_params.get('search')

        if search:
            queryset=queryset.filter(name__icontains=search)
            return queryset
        




        