from rest_framework import serializers
from . models import Ticket


class TicketTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = ['name','description','is_accepted_by_vendor']