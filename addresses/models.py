from django.db import models

# Create your models here.
from accounts.models import Profile


class State(models.Model):
    name = models.CharField(max_length=20)


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='city')
    name = models.CharField(max_length=50)


class Address(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='address')
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='address')
    address = models.TextField()
    post_code = models.CharField(max_length=15)
