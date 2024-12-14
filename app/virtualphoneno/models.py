from django.db import models
from users.models import CustomUser


# Create your models here.
class VirtualPhoneNo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    phone_no = models.CharField(max_length=10, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owner")

    class Meta:
        verbose_name = "Virtual Phoneno"
        verbose_name_plural = "Virtual Phone Numbers"

    def __str__(self):
        return f"{self.phone_no} owned by {self.owner.email}"
