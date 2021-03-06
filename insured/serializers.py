from authenticate.serializers import UserSerializer
from rest_framework import serializers
from .models import Insured


class InsuredSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    supported_insureds = UserSerializer(many=True)

    class Meta:
        model = Insured
        fields = '__all__'
