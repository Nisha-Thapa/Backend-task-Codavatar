from rest_framework import serializers
from .models import VirtualPhoneNumber

class VirtualPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNumber
        fields = [
            "id",
            "phone_number",
            "usage",
            "is_active",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "usage": {"read_only": True},
            "is_active": {"read_only": True},
        }