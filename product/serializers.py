from rest_framework import serializers
from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'get_absolute_url', 'desc', 'price', 'get_image', 'get_preview')

