from django.urls import path
from .views import RegisterView,LoginView,VirtualPhoneNumberListCreateView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('virtual-phone-numbers/', VirtualPhoneNumberListCreateView.as_view(), name='virtual_phone_number_list_create'),
]
