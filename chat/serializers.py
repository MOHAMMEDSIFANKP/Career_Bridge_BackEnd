from rest_framework.serializers import ModelSerializer
from .models import Message
from company.models import ApplyJobs
from api.serializers import UserSerializer
from rest_framework import serializers


# class Messageserializer(ModelSerializer):
#     class Meta:
#         model = Message
#         fields =  '__all__'

class MessageSerializer(ModelSerializer):
    sender_username = UserSerializer()

    class Meta:
        model = Message
        fields = ['message','sender_username']

    def get_sender_username(self,obj):
        return obj.sender.username
    
    