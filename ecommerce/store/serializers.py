from rest_framework import serializers
from .models import Product,CartItem,Cart

# serializing the product model
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class CartItem(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields='__all__'
        