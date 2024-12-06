from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class VirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = ['id', 'number', 'created_at']

class CreateVirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = ['number']

class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = ['id', 'phone_number', 'direction', 'timestamp', 'duration']
