from rest_framework import serializers

from accounts.models import User, Admin, Profile


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password')


class AdminSerializer(serializers.ModelSerializer):
    parent_user = serializers.CharField(source='parent_user.phone_number')

    class Meta:
        model = Admin
        fields = ('id', 'parent_user', 'first_name', 'last_name', 'role')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.phone_number')

    class Meta:
        model = Profile
        read_only_fields = ('user',)
        fields = ('user', 'first_name', 'last_name', 'birth_date', 'email')
