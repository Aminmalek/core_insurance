from authenticate.serializers import UserSerializer
from rest_framework import serializers
from .models import SuperHolder


class SuperHolderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    supported_holders = UserSerializer(many=True)

    class Meta:
        model = SuperHolder
        fields = ['id', 'user', 'supported_holders']
