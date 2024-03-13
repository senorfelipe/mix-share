from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .renderers import AudioMPEGRenderer
from .permissions import IsOwnerOfCommentOrRealOnly, IsOwnerOfMixOrRealOnly
from mixes import service
from mixes.serializer import CommentSerializer, MixSerializer
from mixes.models import Comment, Mix
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import mixins, ModelViewSet, GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


class MixViewSet(ModelViewSet):
    queryset = Mix.objects.all()
    renderer_classes = [JSONRenderer, AudioMPEGRenderer]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = MixSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfMixOrRealOnly]
    lookup_url_kwarg = "mix_id"

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        errors = {}

        try:
            audio_analyzer = service.AudioFileAnalyzer(uploaded_file)
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['length_in_sec'] = audio_analyzer.duration
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                errors.update(serializer.errors)
        except service.AudioAnalysisExeption as e:
            errors.update({'audio_file': 'While processing the audio file an error occured.'})
            # TODO: Add logging output

        return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        mix = get_object_or_404(Mix, id=self.kwargs['mix_id'])
        accept_header = request.headers.get('Accept', '')

        if 'audio/mpeg' in accept_header:
            return service.stream(request, mix.file.path)
        else:
            serializer = self.get_serializer(mix)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfCommentOrRealOnly]
    lookup_url_kwarg = "comment_id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"mix_id": self.kwargs["mix_id"]})
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        return self.queryset.filter(mix_id=self.kwargs["mix_id"])
