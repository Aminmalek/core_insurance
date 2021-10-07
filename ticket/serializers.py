from rest_framework import serializers
from .models import Claim, Ticket
from payment.serializers import InsuranceConnectorSerializer
from authenticate.serializers import UserMinifiedSerializer


class TicketSerializer(serializers.ModelSerializer):
    user = UserMinifiedSerializer()
    class Meta:
        model = Ticket
        fields = '__all__'

class ClaimSerializer(serializers.ModelSerializer):
    user = UserMinifiedSerializer()
    insurance = InsuranceConnectorSerializer()
    class Meta:
        model = Claim
        fields = '__all__'