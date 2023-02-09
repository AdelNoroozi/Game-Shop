from rest_framework import serializers

from accounts.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'password')
