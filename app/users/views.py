from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import CreateUserSerializer
from .models import CustomUser

# Create your views here.


# view to create a user
class CreateUserView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):

        return Response
