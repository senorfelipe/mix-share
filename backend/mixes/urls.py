from django.urls import include, path

from .views import CommentViewSet, MixViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register(r'mixes', MixViewSet, basename="mix")
router.register(r'mixes/(?P<mix_id>[^/.]+)/comments', CommentViewSet, basename="mix-comment")

urlpatterns = [
    path('', include(router.urls)),
]
