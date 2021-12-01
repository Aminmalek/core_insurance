from authenticate.models import User
from.models import Message
from rest_framework import serializers
from authenticate.serializers import UserMinifiedSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserMinifiedSerializer()
    receiver = UserMinifiedSerializer()

    class Meta:
        model = Message
        fields = '__all__'
