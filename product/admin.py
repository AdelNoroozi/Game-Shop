from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin, register, StackedInline

from product.models import Category, Product, ProductImage, ProductEnumProperty, ProductPropertyState, ProductProperty, \
    ProductPropertyValue, Review


class ProductPropertyStateInline(StackedInline):
    model = ProductPropertyState


@register(ProductEnumProperty)
class ProductPropertyAdmin(ModelAdmin):
    inlines = [ProductPropertyStateInline, ]


class ProductEnumPropertyInline(TabularInline):
    model = ProductEnumProperty
    fields = ('name',)
    show_change_link = True


class ProductPropertyInline(TabularInline):
    model = ProductProperty


@register(Category)
class CategoryAdmin(ModelAdmin):
    inlines = [
        ProductEnumPropertyInline,
        ProductPropertyInline
    ]


class ProductPropertyValueInline(TabularInline):
    model = ProductPropertyValue


class ProductImageInline(TabularInline):
    model = ProductImage


@register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductPropertyValueInline
    ]


admin.site.register(Review)
