from rest_framework import serializers
from users.models import CustomUser


# Uses modelSerializer to check CustomUser validate fields and uniqueness
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        ref_name = "User"
        fields = ["username", "date_joined", "email", "password", "phone_no"]


# Login serializer uses serializers only to validate the email and password fields
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_main(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value
