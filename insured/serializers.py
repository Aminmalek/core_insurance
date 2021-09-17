from payment.serializers import InsuranceConnectorSerializer
from payment.models import InsuranceConnector
from authenticate.serializers import UserSerializer
from rest_framework import serializers
from .models import Insured


class InsuredSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    supported_insureds = UserSerializer(many=True)
    insurance = InsuranceConnectorSerializer()

    class Meta:
        model = Insured

        fields = ['id', 'user', 'insurance',
                  'supported_insureds', 'bank_account_number']
