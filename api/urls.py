from django.urls import path
from .views import VirtualPhoneNumberListView, VirtualPhoneNumberCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Token Authentication URLs
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "virtual_numbers/",
        VirtualPhoneNumberListView.as_view(),
        name="virtual-number-list",
    ),
    path(
        "virtual_numbers/create/",
        VirtualPhoneNumberCreateView.as_view(),
        name="virtual-number-create",
    ),
]
