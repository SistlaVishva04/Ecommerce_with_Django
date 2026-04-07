from rest_framework.routers import DefaultRouter
from .models import Product
from .views import ProductViewSet
from django.urls import path
from .views import (CreateCartAPIView,AddToCartAPIView,RemoveFromCartAPIView,ViewCartAPIView)


router=DefaultRouter()
router.register('products',ProductViewSet)

urlpatterns=[
    path('cart/create/',CreateCartAPIView.as_view()),
    path('cart/<int:cart_id>/add/',AddToCartAPIView.as_view()),
    path('cart/<int:cart_id>/remove/<int:product_id>/',RemoveFromCartAPIView.as_view()),
    path('cart/<int:cart_id>/',ViewCartAPIView.as_view())
   
]

urlpatterns+=router.urls

