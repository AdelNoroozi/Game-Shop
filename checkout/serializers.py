from rest_framework import serializers

from checkout.models import Cart, CartItem, Order, Payment
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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'cart', 'final_price', 'discount', 'post', 'address', 'status', 'created_at', 'post_tracking_code')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'type', 'total_price', 'receipt', 'payment_tracking_code')
