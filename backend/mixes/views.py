from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .permissions import IsOwnerOfCommentOrRealOnly, IsOwnerOfMixOrRealOnly
from mixes import service
from mixes.serializer import CommentSerializer, MixSerializer
from mixes.models import Comment, Mix
from rest_framework import status
from rest_framework.viewsets import mixins, generics, ModelViewSet, GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated


class MixViewSet(ModelViewSet):
    queryset = Mix.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = MixSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfMixOrRealOnly]
    lookup_url_kwarg = "mix_id"

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

    def retrieve(self, request, *args, **kwargs):
        # TODO: find good way to stream the audio data
        return super().retrieve(request, *args, **kwargs)



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
