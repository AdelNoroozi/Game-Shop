# from django.db.models import Q
# import jwt
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, UpdateAPIView, ListAPIView
# from rest_framework.decorators import api_view
from rest_framework.decorators import action, api_view
from rest_framework.viewsets import ModelViewSet

from game_shop.permissions import ProductPermissions
from .filters import ProductFilter
from .serializers import ProductSerializer, CategorySerializer, ProductMiniSerializer, ReviewSerializer, \
    ProductUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category, Review
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'desc', 'category__title']
    ordering_fields = ['price', 'title']
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductMiniSerializer
        else:
            return ProductSerializer


class LatestProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:10]
        serializers = ProductMiniSerializer(products, many=True)
        return Response(serializers.data)


class ProductByCategory(ListAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'desc', 'category__title']
    ordering_fields = ['price', 'title']
    pagination_class = PageNumberPagination
    serializer_class = ProductMiniSerializer

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        products = Product.objects.filter(category__slug=category_slug)
        return products


class ProductDetail(RetrieveAPIView, DestroyAPIView, UpdateAPIView):
    permission_classes = (ProductPermissions,)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProductUpdateSerializer
        else:
            return ProductSerializer

    def get_object(self):
        product_slug = self.kwargs.get('product_slug')
        try:
            product = Product.objects.get(slug=product_slug)
        except:
            response = {'message': 'product not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            return product

    #
    # def get(self, request, *args, **kwargs):
    #     category_slug = kwargs.get('category_slug')
    #     product_slug = kwargs.get('product_slug')
    #     try:
    #         category = Category.objects.get(slug=category_slug)
    #     except:
    #         response = {'message': 'category not found'}
    #         return Response(response, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         try:
    #             product = Product.objects.filter(category=category).get(slug=product_slug)
    #         except:
    #             response = {'message': 'product not found'}
    #             return Response(response, status=status.HTTP_404_NOT_FOUND)
    #         else:
    #             self.queryset = product
    #             return super(ProductDetail, self).get(request, *args, **kwargs)
    #
    # def get_object(self):
    #


@api_view(['POST'])
def submit_review(request, category_slug, product_slug):
    try:
        category = Category.objects.get(slug=category_slug)
    except:
        response = {'message': 'category not found'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            product = Product.objects.filter(category=category).get(slug=product_slug)
        except:
            response = {'message': 'product not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            if 'rate' in request.data:
                product = Product.objects.get(slug=product_slug)
                rate = request.data['rate']
                comment = request.data['comment']
                public_name = request.data['public_name']
                review = Review.objects.create(product=product,
                                               public_name=public_name,
                                               rate=rate,
                                               comment=comment)
                serializer = ReviewSerializer(review)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                response = {'bad data'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(RetrieveAPIView):
    serializer_class = CategorySerializer

    def get_object(self):
        category_slug = self.kwargs.get('category_slug')
        try:
            category = Category.objects.get(slug=category_slug)
        except:
            response = {'category not found'}
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        else:
            return category


# @api_view(['POST', ])
# def search(request):
#     string = request.data['string']
#
#     if string:
#         products = Product.objects.filter(
#             Q(title__icontains=string) | Q(desc__icontains=string) | Q(category__title__icontains=string))
#         serializer = ProductMiniSerializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     else:
#         response = {'products': []}
#         return Response(response, status=status.HTTP_204_NO_CONTENT)
