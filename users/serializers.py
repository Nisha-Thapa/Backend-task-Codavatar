from rest_framework import serializers

from .models import CustomUser #importing overridden

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = '__all__' #listing all fields
        
        # you can also specify fields to show
        fields = ["id", "username", "first_name", "last_name", "email"]