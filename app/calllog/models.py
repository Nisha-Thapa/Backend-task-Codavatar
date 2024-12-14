from django.db import models
from users.models import CustomUser
from virtualphoneno.models import VirtualPhoneNo


# Create your models here.
class CallLog(models.Model):
    called_by = models.ForeignKey(
        CustomUser, related_name="called_by", on_delete=models.CASCADE
    )
    called_no = models.ForeignKey(
        VirtualPhoneNo,
        related_name="called_no",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    received_no = models.ForeignKey(
        VirtualPhoneNo,
        related_name="received_no",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    called_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()

    class Meta:
        verbose_name = "Call Log"
        verbose_name_plural = "Call Logs"

    def __str__(self):
        return f"Call from {self.called_no.phone_no} to {self.received_no.phone_no} at {self.called_at}"
