from django.contrib import admin

from product.models import Category, Product, ProductImage

admin.site.register(Category)


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline
    ]
