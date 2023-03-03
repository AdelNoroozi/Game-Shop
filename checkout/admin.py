from django.contrib import admin

# Register your models here.
from checkout.models import *


class CartItemInline(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItemInline,
    ]


admin.site.register(Discount)
admin.site.register(Post)
admin.site.register(Order)
admin.site.register(Payment)
