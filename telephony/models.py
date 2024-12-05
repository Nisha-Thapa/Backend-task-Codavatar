from django.db import models

from users import models as user_models

# Create your models here.
class VirtualPhoneNumber(models.Model):
    user = models.ForeignKey(user_models.CustomUser, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=15, unique=True) #using charfield to store country code with '+'

    def __str__(self):
        return self.number

class CallLog(models.Model):
    phone_number = models.ForeignKey(VirtualPhoneNumber, on_delete=models.CASCADE, related_name='call_logs')
    direction = models.CharField(max_length=10, choices=(('Incoming', 'Incoming'), ('Outgoing', 'Outgoing')))
    duration = models.PositiveIntegerField(default=10)  # Duration in seconds
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.direction} call on {self.phone_number}"
