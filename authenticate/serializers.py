from django.contrib.auth.models import Permission 
from rest_framework import serializers
from .models import User


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username','cash','user_permissions', 
                  'type', 'is_active', 'phone', 'bank_account_number')


class UserMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'type')
