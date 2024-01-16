from rest_framework.response import Response
from mixes import service
from mixes.serializer import MixSerializer
from mixes.models import Mix
from rest_framework import status
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class MixListRetreiveCreateDestroyViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Mix.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = MixSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')

        if service.is_valid_file(uploaded_file.name):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                lenght_in_sec = service.get_mix_length_in_sec(uploaded_file)
                serializer.validated_data['length_in_sec'] = lenght_in_sec
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # only allowed if user is owner
        return super().destroy(request, *args, **kwargs)
