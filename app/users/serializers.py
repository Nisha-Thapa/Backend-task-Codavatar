from rest_framework import serializers
from users.models import CustomUser


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        ref_name = "User"
        fields = ["username", "date_joined", "email", "password", "phone_no"]


class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    def validate_main(self,value):
        try:
            user=CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value
