from django.urls import path, include
from rest_framework import routers
# from rest_framework_nested import routers

from product import views

router = routers.DefaultRouter()
router.register('', views.ProductViewSet)
# routers.NestedDefaultRouter(router, '',)
# router.register('users', UserViewSet)
urlpatterns = [
    path('products/', include(router.urls)),
    path('latest_products/', views.LatestProductList.as_view()),
    # path('search/', views.search),
    path('<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('<slug:category_slug>/<slug:product_slug>/submit_review/', views.submit_review),
]
