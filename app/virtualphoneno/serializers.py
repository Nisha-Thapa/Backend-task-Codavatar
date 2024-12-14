from rest_framework import serializers
from virtualphoneno.models import VirtualPhoneNo


class CreateNo(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNo
        ref_name = "CreateNo"
        fields = "__all__"


class ViewNo(serializers.ModelSerializer):
    class Meta:
        model = VirtualPhoneNo
        ref_name = "ViewNo"
        fields = ["phone_no"]
