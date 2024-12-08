from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from authentication.models import User


class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)