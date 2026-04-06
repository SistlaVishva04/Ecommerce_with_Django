from rest_framework.routers import DefaultRouter
from .models import Product
from .views import ProductViewSet

router=DefaultRouter()
router.register('products',ProductViewSet)
urlpatterns=router.urls
