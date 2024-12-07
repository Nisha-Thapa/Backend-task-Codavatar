from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import VirtualPhoneNumber
from .serializers import VirtualPhoneNumberSerializer


class VirtualPhoneNumberListView(generics.ListAPIView):
    """
    API endpoint to list virtual phone numbers for the authenticated user.

    Permissions:
    - Requires user authentication

    Returns:
    - List of virtual phone numbers owned by the current user
    """

    serializer_class = VirtualPhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve virtual phone numbers specific to the authenticated user.

        Returns:
            QuerySet: Filtered virtual phone numbers for the current user
        """
        return VirtualPhoneNumber.objects.filter(user=self.request.user)


class VirtualPhoneNumberCreateView(generics.CreateAPIView):
    """
    API endpoint to create a new virtual phone number for the authenticated user.

    Permissions:
    - Requires user authentication

    Returns:
    - Newly created virtual phone number details
    """

    serializer_class = VirtualPhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Associate the new virtual phone number with the current authenticated user.

        Args:
            serializer: Serializer instance with validated data
        """
        serializer.save(user=self.request.user)
