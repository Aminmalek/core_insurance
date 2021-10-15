from rest_framework import serializers
from . models import Insurance


class InsuranceSerializer(serializers.ModelSerializer):
    register_form = serializers.JSONField()
    claim_form = serializers.JSONField()
    class Meta:
        model = Insurance
        fields = '__all__'
