from rest_framework import serializers
from .models import VirtualPhoneNumber


class VirtualPhoneNumberSerializer(serializers.ModelSerializer):
    """
    Serializer for Virtual Phone Number model.

    Handles validation and serialization of virtual phone numbers.
    Ensures unique phone numbers and associates with current user.
    """

    class Meta:
        model = VirtualPhoneNumber
        fields = ["id", "phone_number", "is_active"]
        read_only_fields = ["id"]

    def validate_phone_number(self, value):
        """
        Custom validation for phone number:
        1. Checks if phone number already exists
        2. Ensures number is unique across all virtual numbers

        Args:
            value (str): Phone number to validate

        Returns:
            str: Validated phone number

        Raises:
            serializers.ValidationError: If phone number already exists
        """
        # Check if phone number is already in use
        if VirtualPhoneNumber.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")

        return value

    def create(self, validated_data):
        """
        Custom create method to ensure the virtual number is associated
        with the current authenticated user.

        Args:
            validated_data (dict): Validated serializer data

        Returns:
            VirtualPhoneNumber: Newly created virtual phone number instance
        """
        # Retrieve the current authenticated user from the request context
        user = self.context["request"].user

        # Create the virtual phone number and associate with user
        virtual_number = VirtualPhoneNumber.objects.create(user=user, **validated_data)

        return virtual_number
