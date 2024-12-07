from rest_framework.routers import DefaultRouter
from .views import UserViewSet, VirtualPhoneNumberViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'virtual-numbers', VirtualPhoneNumberViewSet)

urlpatterns = router.urls
