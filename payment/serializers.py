from insurance.serializers import InsuranceSerializer
from payment.models import InsuranceConnector, Payment
from authenticate.serializers import UserSerializer
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'is_successfull', 'payment_code', 'insurance', 'user')


class InsuranceConnectorSerializer(serializers.ModelSerializer):
    insurance = InsuranceSerializer()
    supported_insureds = UserSerializer(many=True)
    payment = PaymentSerializer()

    class Meta:
        model = InsuranceConnector

        fields = ('id', 'insurance', 'supported_insureds', 'payment')
