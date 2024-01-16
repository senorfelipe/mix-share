from django.urls import include, path

from .views import MixListRetreiveCreateDestroyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register(r'mixes', MixListRetreiveCreateDestroyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
