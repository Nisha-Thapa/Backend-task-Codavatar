from django.urls import path
from .views import RegisterView,LoginView,VirtualPhoneNumberListCreateView,VirtualPhoneNumberDetailView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('virtual-phone-numbers/', VirtualPhoneNumberListCreateView.as_view(), name='virtual_phone_number_list_create'),
    path('virtual-phone-numbers/<int:pk>/', VirtualPhoneNumberDetailView.as_view(), name='virtual_phone_number_detail'),
]
