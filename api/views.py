from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import VirtualPhoneNumber
from .serializers import VirtualPhoneNumberSerializer


class VirtualPhoneNumberListView(generics.ListAPIView):
    serializer_class = VirtualPhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VirtualPhoneNumber.objects.filter(user=self.request.user)


class VirtualPhoneNumberCreateView(generics.CreateAPIView):
    serializer_class = VirtualPhoneNumberSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
