from rest_framework import serializers

from checkout.models import Cart, CartItem, Order, Payment, Discount, Post
from product.models import Product
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

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('product does not exist')
        else:
            return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        count = self.validated_data['count']
        try:
            cart_item = CartItem.objects.get(product_id=product_id, cart__id=cart_id)
            cart_item.count += count
            cart_item.save()
            self.instance = cart_item

        except:
            self.instance = CartItem.objects.create(product_id=product_id, cart_id=cart_id, count=count)
        return self.instance

    class Meta:
        model = CartItem
        fields = ('id', 'product_id', 'count')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'cart', 'final_price', 'discount', 'post', 'address', 'status', 'created_at', 'post_tracking_code')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'type', 'total_price', 'receipt', 'payment_tracking_code')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'title', 'code', 'is_active', 'discount_percent', 'specific_user')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'name', 'cost', 'deliver_time')
