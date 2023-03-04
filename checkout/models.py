import uuid

from django.db import models

from accounts.models import User
from addresses.models import Address
from product.models import Product


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        cart_items = CartItem.objects.filter(cart=self)
        total = sum([item.count * item.product.price for item in cart_items])
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    count = models.PositiveSmallIntegerField(default=0)


class Post(models.Model):
    name = models.CharField(max_length=20)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    deliver_time = models.CharField(max_length=10)


class Discount(models.Model):
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=False)
    discount_percent = models.IntegerField(default=0)
    specific_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discounts', blank=True, null=True)

    def is_specific_for_a_user(self):
        return bool(self.specific_user is not None)


class Order(models.Model):
    STATUS = (('RTP', 'ready to pay'),
              ('PAD', 'paid'),
              ('PRP', 'preparing'),
              ('PST', 'posting'),
              ('DLV', 'delivered'),
              ('CON', 'confirmed'),
              ('REJ', 'rejected'))
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='orders')
    final_price = models.DecimalField(max_digits=6, decimal_places=2)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='orders')
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, related_name='orders', blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(choices=STATUS, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    post_tracking_code = models.CharField(max_length=20, blank=True, null=True)

    def get_payment_tracking_code(self):
        payment = Payment.objects.filter(order=self, type='IN').first()
        return payment.payment_tracking_code

    def get_return_payment_tracking_code(self):
        if not self.status == 'REJ':
            return None
        else:
            payment = Payment.objects.filter(order=self, type='RTN').first()
            return payment.payment_tracking_code


class Payment(models.Model):
    TYPES = (('IN', 'income'),
             ('RTN', 'return'))
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='payments')
    type = models.CharField(choices=TYPES, max_length=10)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    receipt = models.TextField()
    payment_tracking_code = models.CharField(max_length=20)
