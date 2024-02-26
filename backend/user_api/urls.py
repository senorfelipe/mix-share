from django.urls import include, path
from .views import (
    CookieTokenRefreshView,
    FollowersListView,
    RegistrationAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserFollowView,
    UserProfileViewSet,
)
from rest_framework.routers import DefaultRouter
profile_router = DefaultRouter(trailing_slash=False)
profile_router.register(r'users', UserProfileViewSet)

urlpatterns = [
    path('', include(profile_router.urls)),
    path('users/<int:follower_id>/follow/<int:followee_id>', UserFollowView.as_view()),
    path('users/<int:user_id>/followers', FollowersListView.as_view(), name="user-followers"),
   
    path('auth/token/refresh', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register', RegistrationAPIView.as_view(), name='register'),
    path('auth/login', LoginAPIView.as_view(), name='login'),
    path('auth/logout', LogoutAPIView.as_view(), name='logout'),
]
