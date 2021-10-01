from rest_framework import serializers
from .models import Claim, Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['id', 'name', 'user', 'description', 'is_accepted_by_vendor',
                  'is_accepted_by_company', 'has_withdrawed']

class ClaimSerializer(serializers.ModelSerializer):

    class Meta:
        model = Claim
        fields = '__all__'