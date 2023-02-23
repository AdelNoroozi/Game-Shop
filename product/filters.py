from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from .models import Product


class ProductFilter(FilterSet):
    props = CharFilter
    class Meta:
        model = Product
        fields = {
            'price': ['gt', 'lt'],
            'props': ['exact'],
        }
