from rest_framework import serializers
from .models import Insurance, Coverage


class CoverageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coverage
        fields = '__all__'


class InsuranceSerializer(serializers.ModelSerializer):
    register_form = serializers.JSONField()
    coverage = CoverageSerializer(many=True)

    class Meta:
        model = Insurance
        fields = '__all__'
