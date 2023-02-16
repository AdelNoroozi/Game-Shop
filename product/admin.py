from django.contrib import admin

from product.models import Category, Product, ProductImage, ProductProperty, ProductPropertyValue


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty


class ProductPropertyValueInline(admin.TabularInline):
    model = ProductPropertyValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductPropertyValueInline
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        ProductPropertyInline
    ]
