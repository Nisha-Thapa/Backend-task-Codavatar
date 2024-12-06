from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *

@api_view(['POST'])
def create_virtual_num(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"error":"User not found"})
    if request.method == 'POST':
        seralizer = CreateVirtualPhoneNumberSerializer(data=request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data)

@api_view(['POST'])
def create_user(request):
    if request.method == "POST":
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
@api_view(['GET'])
def get_virtual_num(request):
    get_virtual = VirtualPhoneNumber.objects.all()
    serializer = VirtualPhoneNumberSerializer(get_virtual, many = True)
    return Response(serializer.data)