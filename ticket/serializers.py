from rest_framework import serializers
from .models import Claim, Ticket, ReviewerTimeline
from payment.serializers import InsuranceConnectorSerializer
from authenticate.serializers import UserMinifiedSerializer


class TicketSerializer(serializers.ModelSerializer):
    user = UserMinifiedSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'


class ReviewerTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewerTimeline
        fields = ['date', 'changed_by', 'reviewer']


class ClaimSerializer(serializers.ModelSerializer):
    user = UserMinifiedSerializer()
    insurance = InsuranceConnectorSerializer()
    reviewer_timeline = ReviewerTimelineSerializer(many=True)

    class Meta:
        model = Claim
        fields = '__all__'
