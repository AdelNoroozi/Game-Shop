from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
import re
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, phone_number, is_active=True, is_staff=False, password=None):
        phone_number_pattern = re.compile(r'^(09)\d{9}$')
        if not phone_number:
            raise ValueError('phone number is required')
        if not phone_number_pattern.match(phone_number):
            raise ValueError('phone number is invalid')
        if not password:
            raise ValueError('password is required')
        user_obj = self.model(
            phone_number=phone_number
        )
        user_obj.password = make_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_admin(self, phone_number, password=None, ):
        user = self.create_user(
            phone_number=phone_number,
            password=password
        )
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, ):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
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
    is_active = models.BooleanField(default=True)
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number


class Admin(models.Model):
    roles = (('RM', 'review manager'),
             ('SM', 'shop manager'),
             ('UM', 'user manager'),
             ('OM', 'order manager'),)
    parent_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    role = models.CharField(max_length=10, choices=roles)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.role}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.phone_number} profile'
