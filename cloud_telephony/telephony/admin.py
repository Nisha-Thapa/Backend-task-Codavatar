from django.contrib import admin
from .models import User, VirtualPhoneNumber, CallLog

admin.site.register(User)
admin.site.register(VirtualPhoneNumber)
admin.site.register(CallLog)
