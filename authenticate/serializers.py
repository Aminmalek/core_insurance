from rest_framework import serializers
from . models import User, Type



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'type_name']
