from django.contrib.auth.models import Permission
from rest_framework import serializers
from .models import User
from rest_framework import exceptions
from django.core.validators import RegexValidator


phone_regex = RegexValidator(regex=r'^\d{10}$', message=(
    'Phone number must be like this'" '9137866088'. 10 digits allowed."))


class SignupSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone = serializers.IntegerField()
    bank_account_number = serializers.CharField(max_length=26)

    def password_validation(self, password):
        if not len(password) > 6:
            raise exceptions.ValidationError(
                detail=('Password must be above 6 numbers'))
        if not any(ch.isdigit() for ch in password):
            raise exceptions.ValidationError(
                detail=('Password must contain digit.'))
        if not any(ch.isalpha() for ch in password):
            raise exceptions.ValidationError(
                detail=('Password must contain at least one letter .'))
        return password

    def create(self, validated_data):
        password = validated_data['password']
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=30)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'cash', 'type', 'is_active', 'phone', 'bank_account_number')


class UserMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'type')
