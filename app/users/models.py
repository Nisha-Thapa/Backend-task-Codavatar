from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# custom user model that abstracts django basic user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Enforce unique emails
    phone_no = models.CharField(max_length=10, unique=True)
    REQUIRED_FIELDS = [
        "email"
    ]  # This makes email a required field during user creation

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    # shows email in the admin list for the model
    def __str__(self):
        return self.email
