from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from posts.models import Post, Group
from .permissions import AuthorEditOnly
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
)


class PostVS(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return super().get_permissions()
        else:
            return (permissions.IsAuthenticated(), AuthorEditOnly(),)

    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupVS(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentVS(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):

        if self.request.method == 'GET':
            return super().get_permissions()
        else:
            return (permissions.IsAuthenticated(), AuthorEditOnly(),)

    def main_post(self):
        return get_object_or_404(Post, pk=int(self.kwargs['id_post']))

    def get_queryset(self):
        return self.main_post().comments

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.main_post())


class FollowVS(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('$following__username',)

    def get_permissions(self):
        return (permissions.IsAuthenticated(), AuthorEditOnly(),)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
