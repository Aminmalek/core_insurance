from authenticate.serializers import UserSerializer
from rest_framework import serializers
from .models import Insured
from authenticate.models import User


class InsuredSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    supported_insureds = UserSerializer()

    class Meta:
        model = Insured

        fields = ['id', 'user', 'insurance',
                  'supported_insureds', 'bank_account_number']
