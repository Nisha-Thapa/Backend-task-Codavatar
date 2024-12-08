from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ["created_at", "updated_at"]
        get_latest_by = "created_at"