from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserListSerializer

#apiview for listing and creating users
class UsersListCreate(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.data)
        serializer = UserListSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = {
                "id": instance.id,
                "message": f"User with username {instance.username} created successfully"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"error": str(serializer.errors)})