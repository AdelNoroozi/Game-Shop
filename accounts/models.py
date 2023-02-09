from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
import re
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, phone_number, is_active=True, is_staff=False, first_name=None, last_name=None, password=None):
        phone_number_pattern = re.compile(r'^(09)\d{9}$')
        if not phone_number:
            raise ValueError('phone number is required')
        if not phone_number_pattern.match(phone_number):
            raise ValueError('phone number is invalid')
        if not password:
            raise ValueError('password is required')
        if not first_name:
            raise ValueError('first_name is required')
        if not last_name:
            raise ValueError('last_name is required')
        user_obj = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.password = make_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, phone_number, first_name=None, last_name=None, password=None, ):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    phone_regex_validator = RegexValidator(
        regex=r'^(09)\d{9}$',
        message='invalid phone number'
    )
    phone_number = models.CharField(validators=[phone_regex_validator], max_length=20,
                                    null=False, blank=False, unique=True)
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.phone_number


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
