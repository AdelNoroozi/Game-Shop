from django.urls import path, include
from rest_framework import routers

from cart.views import CartViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register('cart', CartViewSet)
# router.register('items', CartItemViewSet)
urlpatterns = [
    path('', include(router.urls))
]
