from rest_framework import serializers

from addresses.models import Address


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')
    user = serializers.CharField(source='user.phone_number')

    class Meta:
        model = Address
        fields = ('id', 'city', 'user', 'address', 'post_code')
