from django.urls import include, path
from .views import RegistrationAPIView, LoginAPIView, LogoutAPIView, UserProfileViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

profile_router = DefaultRouter(trailing_slash=False)
profile_router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(profile_router.urls)),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
]
