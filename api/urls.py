from django.urls import path, include
from rest_framework import routers

from api.views import ProductViewSet, WarehouseViewSet

router = routers.SimpleRouter()

router.register('warehouses', WarehouseViewSet, basename='warehouses')
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
