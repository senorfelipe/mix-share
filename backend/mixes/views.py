from rest_framework.response import Response
from mixes import service
from mixes.serializer import MixSerializer
from mixes.models import Mix
from rest_framework import status
from rest_framework import viewsets


class MixViewSet(viewsets.ModelViewSet):
    queryset = Mix.objects.all()
    serializer_class = MixSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("file")
        if service.is_valid_file(uploaded_file.name):
            data = request.data
            lenght_in_sec = service.get_mix_length_in_sec(uploaded_file)
            data["lenght_in_sec"] = lenght_in_sec
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                print(f"\n\ndata: \n{serializer.validated_data}\n\n\n")
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
