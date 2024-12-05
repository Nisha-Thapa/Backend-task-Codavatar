from rest_framework import serializers

from .models import CustomUser 
from telephony import serializers as telephony_serializers

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = '__all__' #listing all fields
        
        # you can also specify fields to show
        fields = ["id", "username", "first_name", "last_name", "email"]
        

class UsersVirtualPhoneNumberListing(serializers.ModelSerializer):
    phone_numbers = telephony_serializers.VirtualPhoneNumberSerializer(many=True)
    
    class Meta:
        model = CustomUser
        fields = ["id", "username", "phone_numbers"]