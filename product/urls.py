from django.urls import path, include
from rest_framework import routers

from product import views

router = routers.DefaultRouter()
# router.register('users', UserViewSet)
urlpatterns = [
    path('latest-products/', views.LatestProductList.as_view()),
    path('products/search/', views.search),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),

]
