from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductPropertyState, ProductEnumProperty


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class PropSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.name')

    class Meta:
        model = ProductPropertyState
        fields = ('property_name', 'state')


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    props = PropSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'desc', 'price', 'images', 'props')


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'get_thumbnail')


class CategorySerializer(serializers.ModelSerializer):
    products = ProductMiniSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'desc', 'products')
