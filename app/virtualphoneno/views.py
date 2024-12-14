from rest_framework.response import Response
from virtualphoneno.models import VirtualPhoneNo
from users.models import CustomUser
from virtualphoneno.serializers import CreateNo, ViewNo
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from django.shortcuts import get_object_or_404

# Create your views here.


# view to create a virtualPhoneNo
class CreateNoView(APIView):
    serializer_class = CreateNo

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get("owner")
        user = get_object_or_404(CustomUser, username=username)

        newNoData = {"phone_no": data.get("phone_no"), "owner": user.id}

        serializer = self.serializer_class(data=newNoData)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


# view to show the virtualPhoneNo associated with the user
class ShowNoView(APIView):
    serializer_class = ViewNo

    def get(self, request, *args, **kwargs):
        data = request.data
        virtualNumbers = VirtualPhoneNo.objects.filter(owner__email=data["email"])
        serializer = self.serializer_class(virtualNumbers, many=True)
        return Response({"virtual_numbers": serializer.data})
