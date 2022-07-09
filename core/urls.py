from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from core.viewsets import UserViewSet

router = DefaultRouter()
router.register(r'auth/user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    # AUTH JWT
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
