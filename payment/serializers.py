from insurance.serializers import InsuranceSerializer
from payment.models import InsuranceConnector
from authenticate.serializers import UserSerializer
from rest_framework import serializers


class InsuranceConnectorSerializer(serializers.ModelSerializer):
    insurance = InsuranceSerializer()
    user = UserSerializer()

    class Meta:
        model = InsuranceConnector
        fields = ('id', 'user', 'insurance', 'is_accepted_by_company', 'is_paid', 'payment_code')
