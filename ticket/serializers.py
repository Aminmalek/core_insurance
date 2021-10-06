from rest_framework import serializers
from .models import Claim, Ticket
from payment.serializers import InsuranceConnectorSerializer

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'

class ClaimSerializer(serializers.ModelSerializer):
    insurance = InsuranceConnectorSerializer()
    class Meta:
        model = Claim
        fields = '__all__'