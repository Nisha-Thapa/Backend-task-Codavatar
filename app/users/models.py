from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Enforce unique emails
    phone_no = models.CharField(max_length=10, unique=True)
    REQUIRED_FIELDS = [
        "email"
    ]  # This makes email a required field during user creation

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
