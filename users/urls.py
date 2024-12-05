from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UsersListCreate.as_view()),
    path('user/<int:pk>/phone-numbers/', views.VirtualPhoneNumberView.as_view()) # indicates phone numbers owned by a users 
]
