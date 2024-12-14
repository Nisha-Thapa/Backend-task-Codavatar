from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED
from users.serializers import CreateUserSerializer
from .models import CustomUser
# Create your views here.


# view to create a user
class CreateUserView(APIView):
    serializer_class=CreateUserSerializer
    def post(self,request,*args,**kwargs):
        data=request.data
        print(data)
        serializer=self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        user.set_password(data['password'])
        user.save()
        return Response(serializer.data,status=HTTP_201_CREATED)