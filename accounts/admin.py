from django.contrib import admin

from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User, Admin, Profile


class UserAdmin(admin.ModelAdmin):
    search_fields = ['phone_number', 'first_name', 'last_name']
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    class Meta:
        model = User


user = get_user_model()

admin.site.register(user, UserAdmin)
admin.site.register(Admin)
admin.site.register(Profile)
