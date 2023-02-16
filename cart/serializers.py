from rest_framework import serializers

from cart.models import Cart, CartItem
from product.serializers import ProductMiniSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(many=False)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'count')


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_price')

    def get_total_price(self, cart):
        items = cart.items.all()
        total = sum([item.count * item.product.price for item in items])
        return total


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ('id', 'product_id', 'quantity')
