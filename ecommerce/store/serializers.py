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
        
# serializing the cart model
class Cart(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'


# creating a add to cart serializer 
class AddtoCartSerializer(serializers.Serializer):
    
    product_id=serializers.IntegerField()
    quantity=serializers.IntegerField()
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
    