"""
Django models for the Cloud Telephony API.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Adds additional validation for contact number and allows
    more flexible user management.

    Fields:
    - Inherits all fields from AbstractUser
    - contact_number: Optional unique phone number with validation
    """

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
    """
    Represents a virtual phone number associated with a user.

    This model allows users to have multiple virtual phone numbers
    with active/inactive status.

    Fields:
    - phone_number: Unique validated phone number
    - user: Foreign key to the User who owns the number
    - is_active: Flag to enable/disable the virtual number
    """

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

    def __str__(self):
        """String representation of the virtual phone number."""
        return f"{self.phone_number} (User: {self.user.username})"


class CallLog(models.Model):
    """
    Tracks logs for phone calls made or received by virtual phone numbers.

    Captures details of each call including direction, duration,
    and involved phone numbers.

    Fields:
    - virtual_phone_number: The virtual number involved in the call
    - timestamp: Automatic recording of call time
    - direction: Incoming or outgoing call
    - duration: Length of the call in seconds
    - caller_number: Number initiating the call
    - called_number: Number receiving the call
    """

    DIRECTION_CHOICES = [("IN", "Incoming"), ("OUT", "Outgoing")]
    virtual_phone_number = models.ForeignKey(
        VirtualPhoneNumber, on_delete=models.CASCADE, related_name="call_logs"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    duration = models.PositiveIntegerField()
    caller_number = models.CharField(max_length=15, default="")
    called_number = models.CharField(max_length=15, default="")

    def __str__(self):
        """String representation of the call log."""
        return (
            f"{self.direction} call on {self.timestamp} via {self.virtual_phone_number}"
        )
