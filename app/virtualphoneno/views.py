from rest_framework.response import Response
from virtualphoneno.models import VirtualPhoneNo
from virtualphoneno.serializers import CreateNo, ViewNo
from rest_framework.views import APIView

# Create your views here.


# view to create a virtualPhoneNo
class CreateNoView(APIView):
    serializer_class = CreateNo

    def post(self, request, *args, **kwargs):

        return Response


# view to show the virtualPhoneNo associated with the user
class ShowNoView(APIView):
    serializer_class = ViewNo

    def get(self, request, *args, **kwargs):

        return Response
