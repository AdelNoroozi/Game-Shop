from django.contrib.admin import TabularInline, ModelAdmin, register, StackedInline

from product.models import Category, Product, ProductImage, ProductEnumProperty, ProductPropertyState


class ProductPropertyStateInline(StackedInline):
    model = ProductPropertyState


@register(ProductEnumProperty)
class ProductPropertyAdmin(ModelAdmin):
    inlines = [ProductPropertyStateInline, ]


class ProductPropertyInline(TabularInline):
    model = ProductEnumProperty
    fields = ('name',)
    show_change_link = True


@register(Category)
class CategoryAdmin(ModelAdmin):
    inlines = [
        ProductPropertyInline
    ]


class ProductImageInline(TabularInline):
    model = ProductImage


@register(Product)
class ProductAdmin(ModelAdmin):
    inlines = [
        ProductImageInline,
    ]
