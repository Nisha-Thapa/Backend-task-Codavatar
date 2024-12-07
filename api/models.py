from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    phone_number_validator = RegexValidator(
        regex=r"^\+?1?\d{9,15}$", message="Phone number must be 9-15 digits"
    )
    contact_number = models.CharField(
        validators=[phone_number_validator],
        max_length=16,
        unique=True,
        blank=True,
        null=True,
    )


class VirtualPhoneNumber(models.Model):
    phone_number_validator = RegexValidator(
        regex=r"^\+?1?\d{9,15}$", message="Phone number must be 9-15 digits"
    )
    phone_number = models.CharField(
        max_length=15, unique=True, validators=[phone_number_validator]
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="virtual_numbers"
    )
    is_active = models.BooleanField(default=True)


class CallLog(models.Model):
    DIRECTION_CHOICES = [("IN", "Incoming"), ("OUT", "Outgoing")]
    virtual_phone_number = models.ForeignKey(
        VirtualPhoneNumber, on_delete=models.CASCADE, related_name="call_logs"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    duration = models.PositiveIntegerField()
    caller_number = models.CharField(max_length=15, default="")
    called_number = models.CharField(max_length=15, default="")
