from rest_framework.response import Response
from mixes import service
from mixes.serializer import MixSerializer
from mixes.models import Mix
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class ListCreateMix(ListCreateAPIView):
    queryset = Mix.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = MixSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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


class RetrieveDestroyMix(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Mix.objects.all()
    serializer_class = MixSerializer
