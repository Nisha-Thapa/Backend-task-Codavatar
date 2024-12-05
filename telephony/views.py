from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers, models
from users import models as user_models
from users import serializers as user_serializers
# Create your views here.

class VirtualPhoneNumberView(APIView):
    def get_user(self, pk):
        #using prefetch_related to avoid N+1 query problem
        return user_models.CustomUser.objects.prefetch_related('phone_numbers').get(id=pk)
    
    def get(self, request, pk):
        user = self.get_user(pk)
        serializer = user_serializers.UsersVirtualPhoneNumberListing(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
