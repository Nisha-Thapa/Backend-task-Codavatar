from rest_framework import generics, permissions
from .serializers import VirtualPhoneNumberSerializer
from .models import VirtualPhoneNumber

from django.db import transaction
from django.contrib.auth.models import AnonymousUser

from drf_spectacular.utils import extend_schema, OpenApiResponse

class VirtualPhoneNumberView(generics.ListCreateAPIView):
    serializer_class = VirtualPhoneNumberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return VirtualPhoneNumber.objects.none()
        return VirtualPhoneNumber.objects.filter(user = self.request.user).order_by('-created_at')
    
    @extend_schema(
        summary="List virtual phone numbers",
        description="This endpoint allows authenticated users to list their virtual phone numbers.",
        responses={
            200: VirtualPhoneNumberSerializer(many=True),
            401: OpenApiResponse(
                    response={
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string", "example": "Authentication credentials were not provided."}
                        }
                    },
                    description="Unauthorized access"
                ),
            }
        )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create virtual phone numbers",
        description="This endpoint allows authenticated users to create a new virtual phone number.",
        responses={
            200: VirtualPhoneNumberSerializer,
            401: OpenApiResponse(
                    response={
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string", "example": "Authentication credentials were not provided."}
                        }
                    },
                    description="Unauthorized access"
                ),
            }
        )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)