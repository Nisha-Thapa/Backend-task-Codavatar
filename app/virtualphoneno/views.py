from rest_framework.response import Response
from virtualphoneno.models import VirtualPhoneNo
from users.models import CustomUser
from virtualphoneno.serializers import CreateNo, ViewNo
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.


# view to create a virtualPhoneNo
class CreateNoView(APIView):
    serializer_class = CreateNo

    # uses django TokenAuthentication. needs client to send token in header as Token <tokenkey>
    authentication_classes = [TokenAuthentication]
    # checks authentication only lets reqeust process when authenticated
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        # takes username as input to check the availability of user
        username = data.get("username")


        # checks availability of user
        user = get_object_or_404(CustomUser, username=username)

        # setting structure for serializer
        newNoData = {"phone_no": data.get("phone_no"), "owner": user.id}

        serializer = self.serializer_class(data=newNoData)
        
        # checks structure and fields according to the model
        serializer.is_valid(raise_exception=True)
        
        # saves the data in database
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


# view to show the virtualPhoneNo associated with the user


class ShowNoView(APIView):
    serializer_class = ViewNo
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = request.data
        # takes user as a field to get the ownerfield in virtualnumbers
        virtualNumbers = VirtualPhoneNo.objects.filter(owner__username=data["username"])
        serializer = self.serializer_class(virtualNumbers, many=True)
        return Response({"virtual_numbers": serializer.data})
