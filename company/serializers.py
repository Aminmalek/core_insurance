from rest_framework import serializers
from ticket.models import Ticket


class TicketForCompanySerializer(serializers.ModelSerializer):
    def get_user_name(self, obj):
        return obj.user.username

    username = serializers.SerializerMethodField("get_user_name")

    class Meta:
        model = Ticket
        fields = ['name', 'username', 'description', 'is_accepted_by_vendor',
                  'is_accepted_by_company', 'has_withdrawed']
