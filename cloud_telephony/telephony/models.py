from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
class VirtualPhoneNumber(models.Model):
    number = models.CharField(max_length=15, unique=True)
    user = models.ForeignKey(User, related_name='virtual_numbers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number

class CallLog(models.Model):
    virtual_number = models.ForeignKey(VirtualPhoneNumber, related_name='call_logs', on_delete=models.CASCADE)
    call_type = models.CharField(max_length=10, choices=(('incoming', 'Incoming'), ('outgoing', 'Outgoing')))
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()  # Duration in seconds
