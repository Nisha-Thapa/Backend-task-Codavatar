from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from users.serializers import CreateUserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from .models import CustomUser
from rest_framework.generics import get_object_or_404

# Create your views here.


class LogIn(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        print("something")
        serialiser = self.serializer_class(data=data)
        serialiser.is_valid(raise_exception=True)

        user = get_object_or_404(CustomUser, email=data["email"])
        if not user.check_password(data["password"]):
            return Response(HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, HTTP_200_OK)


# view to create a user
class SignUp(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        # will cause raise error if the serializer requirements are not met like duplicate value or missing fields
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(data["password"])
        user.save()

        # creates token to authenticate
        token = Token.objects.create(user=user)
        return Response(
            {"data": serializer.data, "token": token.key}, status=HTTP_201_CREATED
        )
