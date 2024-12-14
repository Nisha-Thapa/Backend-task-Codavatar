from django.urls import path
from users.views import (
    SignUp,LogIn
)
urlpatterns = [
    path("signup",SignUp.as_view(),name="create_user"),
    path("login",LogIn.as_view(),name="login_user")
]