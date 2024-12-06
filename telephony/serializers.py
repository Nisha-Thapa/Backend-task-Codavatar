from rest_framework import serializers
from .models import VirtualPhoneNumber, CallLog

#this serializer is used for list only
class VirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = ['id', 'number']

#this serializer is used for create only
class CreateVirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = ['number', 'user']

class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = ['id', 'phone_number', 'direction', 'duration', 'timestamp']
