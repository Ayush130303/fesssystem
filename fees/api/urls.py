from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    StudentsViewSet,
    FeeStructureViewSet,
    FeePaymentViewSet,
    AnnouncementViewSet,
)
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'students', StudentsViewSet, basename='students')
router.register(r'fee-structure', FeeStructureViewSet, basename='fee-structure')
router.register(r'fee-payments', FeePaymentViewSet, basename='fee-payments')
router.register(r'announcements', AnnouncementViewSet, basename='announcements')

urlpatterns = router.urls
from django.urls import path
# Add token auth endpoint
urlpatterns += [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
