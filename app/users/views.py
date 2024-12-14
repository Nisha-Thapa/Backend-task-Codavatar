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

    # gets email and password as request body and gives token to authenticate for other apis
    def post(self, request, *args, **kwargs):
        data = request.data

        serialiser = self.serializer_class(data=data)
        serialiser.is_valid(raise_exception=True)

        # gets object of email field or returns error
        user = get_object_or_404(CustomUser, email=data["email"])

        # checks if hashed password in model instance matches with the current password
        if not user.check_password(data["password"]):
            return Response(HTTP_404_NOT_FOUND)

        # creates new drf token or if already present sets available token as token
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

        # created instance is saved to user ie user holds the reference to created object
        user = serializer.save()

        # hashes the password
        user.set_password(data["password"])
        user.save()

        # creates drf auth token to authenticate
        token = Token.objects.create(user=user)
        return Response(
            {"data": serializer.data, "token": token.key}, status=HTTP_201_CREATED
        )
