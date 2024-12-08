from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={"input_type": "password"}, validators=[validate_password], trim_whitespace=False)
    confirm_password = serializers.CharField(required=True, style={"input_type": "password"}, trim_whitespace=False)
    
    class Meta:
        fields = [
            "email",
            "password",
            "confirm_password"
        ]
        
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('A user is already registered with this e-mail address.'))
        return email

    def validate(self, attrs):
        super().validate(attrs)
        self.validate_email(attrs['email'])
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        _ = attrs.pop('confirm_password')
        return attrs

    def create(self, validated_data):
        user = User(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True)

    def authenticate(self, **kwargs):
        return authenticate(**kwargs)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = self.authenticate(email=email, password=password)
            if user is None:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        if not user.is_active:
            msg = _('User  account is disabled.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs