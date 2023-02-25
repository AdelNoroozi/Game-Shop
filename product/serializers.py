from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductPropertyState, ProductEnumProperty, ProductPropertyValue, \
    Review


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image')


class PropSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.name')

    class Meta:
        model = ProductPropertyState
        fields = ('property_name', 'state')


class ProductPropertyValueSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='property.name')

    class Meta:
        model = ProductPropertyValue
        fields = ('property_name', 'value')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'public_name', 'rate', 'comment')


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    props = PropSerializer(many=True)
    property_values = ProductPropertyValueSerializer(many=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'desc', 'price', 'get_avg_rating', 'images', 'props', 'property_values', 'reviews')


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'get_thumbnail')


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'desc', 'price',
                  # 'images', 'props', 'property_values'
                  )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductMiniSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'desc', 'products')
