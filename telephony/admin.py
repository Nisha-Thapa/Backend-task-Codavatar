from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.VirtualPhoneNumber)
admin.site.register(models.CallLog)