from django.urls import path, include
from rest_framework import routers

from checkout import views

# from checkout.views import CartViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register('discounts', views.DiscountViewSet)
router.register('posts', views.PostViewSet)
# router.register('carts', CartViewSet)
# router.register('items', CartItemViewSet)
urlpatterns = [
    path('carts/create_cart/', views.CreateOrder.as_view()),
    path('create_order/', views.CreateOrder.as_view()),
    path('create_payment/', views.CreatePayment.as_view()),
    path('', include(router.urls))
]
