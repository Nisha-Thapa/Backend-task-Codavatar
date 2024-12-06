from django.urls import path
from .views import create_virtual_num, create_user, get_virtual_num

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('get_virtual_num/', get_virtual_num, name = 'get_virtual_num'),
    path('users/<int:user_id>/phone-numbers/create/', create_virtual_num, name='create_virtual_phone_number'),
]
