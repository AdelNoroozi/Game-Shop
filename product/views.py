from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product


class LatestGameList(APIView):
    def get(self, request, format=None):
        games = Product.objects.all()[0:10]
        serializers = ProductSerializer(games, many=True)
        return Response(serializers.data)