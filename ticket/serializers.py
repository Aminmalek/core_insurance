from rest_framework import serializers
from .models import Claim, Ticket
from payment.serializers import InsuranceConnectorSerializer
from authenticate.serializers import UserSerializer


class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = '__all__'

class ClaimSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    insurance = InsuranceConnectorSerializer()
    class Meta:
        model = Claim
        fields = '__all__'