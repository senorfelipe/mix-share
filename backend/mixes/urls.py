from django.urls import path

from .views import ListCreateMix, RetrieveDestroyMix

urlpatterns = [
    path('mixes/', ListCreateMix.as_view(), name="mixes"),
    path('mixes/<int:pk>/', RetrieveDestroyMix.as_view(), name="mixe detail"),
]
