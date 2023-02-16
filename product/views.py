from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import ProductSerializer, CategorySerializer, ProductMiniSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category


class LatestProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:10]
        serializers = ProductMiniSerializer(products, many=True)
        return Response(serializers.data)


# class ProductByCategory(APIView):
#     def get(self, request, category_slug):
#         category = get_object_or_404(Category, slug=category_slug)
#         products = Product.objects.filter(category=category)
#         serializers = ProductSerializer(products, many=True)
#         return Response(serializers.data)


class ProductDetail(APIView):

    def get(self, request, category_slug, product_slug):
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
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetail(APIView):
    def get(self, request, category_slug):
        try:
            category = Category.objects.get(slug=category_slug)
        except:
            response = {'message': 'category not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', ])
def search(request):
    string = request.data['string']

    if string:
        products = Product.objects.filter(
            Q(title__icontains=string) | Q(desc__icontains=string) | Q(category__title__icontains=string))
        serializer = ProductMiniSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        response = {'products': []}
        return Response(response, status=status.HTTP_204_NO_CONTENT)
