from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create a schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Cloud Telephony API",
        default_version='v1',
        description="APIs for managing virtual phone numbers and call logs",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
