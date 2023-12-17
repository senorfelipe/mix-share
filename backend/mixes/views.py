from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from mixes.models import Mix


# Create your views here.
def mix_list(request, *args, **kwargs):
    mix_list = Mix.objects.all()
    mixes = [x.serialize() for x in mix_list]
    data = {"response": mixes}
    return JsonResponse(data)


