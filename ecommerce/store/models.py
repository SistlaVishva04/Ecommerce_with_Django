from django.db import models

# Entities needed for the ecommerce store is 
# Product,Cart,CartItem,Order,OrderItem

#Product model
class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.IntegerField()
    stock=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Cart model
class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)

# CartItem model
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()

#Order model
class Order(models.Model):
    create_at=models.DateTimeField(auto_now_add=True)


#OrderItem model
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    

    
