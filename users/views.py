from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers
from telephony import serializers as telephony_serializers

#apiview for listing and creating users
class UsersListCreate(APIView):
    def get(self, request):
        users = models.CustomUser.objects.all()
        serializer = serializers.UserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.data)
        serializer = serializers.UserListSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = {
                "id": instance.id,
                "message": f"User with username {instance.username} created successfully"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({"error": str(serializer.errors)})
    

class UsersVirtualPhoneNumberView(APIView):
    def get_user(self, pk):
        #using prefetch_related to avoid N+1 query problem
        return models.CustomUser.objects.prefetch_related('phone_numbers').get(id=pk)
    
    def get(self, request, pk):
        user = self.get_user(pk)
        serializer = serializers.UsersVirtualPhoneNumberListing(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, pk):
        user = self.get_user(pk) # checking if the user exists
        data = request.data
        data.update({
            'user': pk
        })
        serializer = telephony_serializers.CreateVirtualPhoneNumberSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = {
                'id': instance.id,
                'message': f'Virtual phone number for user "{user.username}" successful'
                #here using user from above fetched so that extra database query is not made
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
        
