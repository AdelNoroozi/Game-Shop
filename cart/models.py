import uuid

from django.db import models

from product.models import Product


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    count = models.IntegerField(default=1)
