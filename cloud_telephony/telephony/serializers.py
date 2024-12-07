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
    # Establish a relationship with VirtualPhoneNumberSerializer
    # `many=True` indicates that a user can have multiple virtual phone numbers
    # `read_only=True` ensures this field cannot be modified through this serializer
    virtual_numbers = VirtualPhoneNumberSerializer(many=True, read_only=True)

    class Meta:
        # Specify the model and fields to include in the serialized output
        model = User
        fields = ['id', 'name', 'email', 'virtual_numbers']

