from django.urls import path
from virtualphoneno.views import CreateNoView, ShowNoView

urlpatterns = [
    path("create", CreateNoView.as_view(), name="Create_virtual_no"),
    path("show", ShowNoView.as_view(), name="show_virtual_no"),
]
