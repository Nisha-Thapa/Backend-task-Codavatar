from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,LoginSerializer,VirtualPhoneNumberSerializer
from rest_framework.permissions import AllowAny
from .models import VirtualPhoneNumber, CallLog
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user registration.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Handles user login by validating email and password.
    Returns access and refresh tokens upon success.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VirtualPhoneNumberListCreateView(ListCreateAPIView):
    """
    List all virtual phone numbers for the authenticated user and create a new one.
    """
    serializer_class = VirtualPhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only the virtual phone numbers belonging to the authenticated user.
        """
        return VirtualPhoneNumber.objects.filter(user=self.request.user)