from django.urls import path

from . import views

urlpatterns = [
    path('', views.UsersListCreate.as_view()),
]
