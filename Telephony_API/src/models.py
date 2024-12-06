from django.db import models

class User(models.Model):
    user = models.CharField(max_length=255, blank=True, default='')
    name = models.CharField(max_length=255, default='', blank=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.name

class VirtualPhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=15, unique=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number

class CallLog(models.Model):
    phone_number = models.ForeignKey(VirtualPhoneNumber, on_delete=models.CASCADE, related_name='call_logs')
    direction = models.CharField(max_length=10, choices=[('INCOMING', 'Incoming'), ('OUTGOING', 'Outgoing')])
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text="Duration in seconds",default=0)

    def __str__(self):
        return f"{self.direction} - {self.phone_number.number}"
