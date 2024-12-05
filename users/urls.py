from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UsersListCreate.as_view()),
    path('users/<int:pk>/phone-numbers/', views.UsersVirtualPhoneNumberView.as_view(), name="list_phone_numbers_user"), # indicates phone numbers owned by a users 
    path('users/<int:pk>/phone-numbers/create/', views.UsersVirtualPhoneNumberView.as_view(), name="create_phone_numbers_user") # indicates phone numbers owned by a users 
]
