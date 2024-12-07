from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, VirtualPhoneNumber
from .serializers import UserSerializer, VirtualPhoneNumberSerializer

# ViewSet for managing User model CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    # Define the queryset to retrieve all User objects
    queryset = User.objects.all()
    # Specify the serializer to be used for User objects
    serializer_class = UserSerializer

# ViewSet for managing VirtualPhoneNumber model CRUD operations
class VirtualPhoneNumberViewSet(viewsets.ModelViewSet):
    # Define the queryset to retrieve all VirtualPhoneNumber objects
    queryset = VirtualPhoneNumber.objects.all()
    # Specify the serializer to be used for VirtualPhoneNumber objects
    serializer_class = VirtualPhoneNumberSerializer

    # Custom action to create a VirtualPhoneNumber for a specific user
    @action(detail=False, methods=['post'], url_path='create-for-user/(?P<user_id>\\d+)')
    def create_for_user(self, request, user_id=None ):
        # Attempt to retrieve the user by ID
        user = User.objects.filter(id=user_id).first()
        if not user:
            # Return a 404 response if the user is not found
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Validate the incoming data using the serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if the phone number already exists
            if VirtualPhoneNumber.objects.filter(number=serializer.validated_data['number']).exists():
                # Return a 400 response if the number is already in use
                return Response({"detail": "Number already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Save the new VirtualPhoneNumber associated with the user
            serializer.save(user=user)
            # Return the serialized data and a 201 status upon successful creation
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return a 400 response with validation errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
