from rest_framework import serializers
from .models import VirtualPhoneNumber, CallLog

class VirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = ['id', 'number']

class CreateVirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = ['number', 'user']

class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = ['id', 'phone_number', 'direction', 'duration', 'timestamp']
