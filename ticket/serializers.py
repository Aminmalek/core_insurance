from rest_framework import serializers
from . models import Ticket


class TicketTypeVendorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = ['name','description','is_accepted_by_vendor']

class TicketTypeCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['name','description','is_accepted_by_vendor']
