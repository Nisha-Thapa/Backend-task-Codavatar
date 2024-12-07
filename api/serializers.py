from rest_framework import serializers
from .models import VirtualPhoneNumber


class VirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = ["id", "phone_number", "is_active"]
        read_only_fields = ["id"]

    def validate_phone_number(self, value):
        if VirtualPhoneNumber.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value
