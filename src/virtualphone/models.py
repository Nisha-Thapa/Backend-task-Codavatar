from django.db import models
from core.base import TimeStamp
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class VirtualPhoneNumber(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='virtual_phone_numbers')
    phone_number = models.CharField(max_length=15, unique=True)
    usage = models.PositiveIntegerField(default=0) # Total time in seconds used in call log
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.phone_number
    
    class Meta:
        db_table = "virtual_phone_numbers"
        verbose_name = _("Virtual Phone Number")
        verbose_name_plural = _("Virtual Phone Numbers")

class CallLog(TimeStamp):
    virtual_phone_number = models.ForeignKey(
        VirtualPhoneNumber, on_delete=models.CASCADE, related_name='logs'
    )
    call_type = models.CharField(max_length=10, choices=(('incoming', 'Incoming'), ('outgoing', 'Outgoing')))
    duration = models.PositiveIntegerField()  # Duration in seconds

    def __str__(self):
        return f"{self.call_type} call on {self.virtual_phone_number.phone_number}"
    
    class Meta:
        db_table = "call_logs"
        verbose_name = _("Call Log")
        verbose_name_plural = _("Call Logs")