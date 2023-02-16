from io import BytesIO

from PIL import Image
from django.core.files import File
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField(default='', blank=True)
    slug = models.SlugField()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        images = ProductImage.objects.filter(product=self)
        thumbnail = None
        for image in images:
            if image.is_thumb:
                thumbnail = image.image.url
        return thumbnail

    def get_category(self):
        return self.category


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    alt_text = models.CharField(max_length=20)
    is_thumb = models.BooleanField(default=False)


class ProductProperty(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_properties')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ProductPropertyValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='property_values')
    Property = models.ForeignKey(ProductProperty,
                                 on_delete=models.CASCADE,
                                 related_name='values')
    value = models.CharField(max_length=50)
