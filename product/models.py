from io import BytesIO

from PIL import Image
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.http import JsonResponse

from accounts.models import User


class Category(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField(default='', blank=True)
    slug = models.SlugField()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_enum_props(self):
        props = ProductPropertyState.objects.filter(property__category=self).values()
        return props


class ProductEnumProperty(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_enum_properties')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ProductPropertyState(models.Model):
    property = models.ForeignKey(ProductEnumProperty, on_delete=models.CASCADE, related_name='product_property_states')
    state = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.property.name} - {self.state}'


class ProductProperty(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_properties')
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.category.title} - {self.name}'


class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    desc = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    props = models.ManyToManyField(ProductPropertyState,
                                   # limit_choices_to={'product__category__title': category.title}
                                   )

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

    # def get_avg_price(self):
    #     avg_price = ProductProviderProp.objects.filter(blank_product=self).aggregate(avg_price=Avg('price'))
    #     return avg_price

    def get_avg_rating(self):
        avg_rating = Review.objects.filter(product=self).aggregate(avg_rating=Avg('rate'))
        return avg_rating


class ProductPropertyValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='property_values')
    property = models.ForeignKey(ProductProperty, on_delete=models.CASCADE, related_name='property_values')
    value = models.CharField(max_length=25)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    alt_text = models.CharField(max_length=20)
    is_thumb = models.BooleanField(default=False)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    public_name = models.CharField(max_length=20, default='Anonymous')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_confirmed = models.BooleanField(default=False)
