from rest_framework.serializers import ModelSerializer
from .models import Message
from company.models import ApplyJobs
from api.serializers import UserSerializer
from rest_framework import serializers


class MessageSerializer(ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message', 'sender_email']
