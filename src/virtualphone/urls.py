from django.urls import path
from .views import VirtualPhoneNumberView

urlpatterns = [
    path("virtual-phone/", VirtualPhoneNumberView.as_view(), name="virtual-phone"),
]
