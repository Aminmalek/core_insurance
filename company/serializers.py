from rest_framework import serializers
from ticket.models import Ticket


class TicketForCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ['name','description','is_accepted_by_vendor','is_accepted_by_company']
