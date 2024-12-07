from rest_framework import serializers
from .models import User, VirtualPhoneNumber

# Serializer for the VirtualPhoneNumber model
class VirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the model and fields to include in the serialized output
        model = VirtualPhoneNumber
        fields = ['id', 'number', 'created_at']

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    virtual_numbers = VirtualPhoneNumberSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'virtual_numbers']


