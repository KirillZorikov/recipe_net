from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.decorators import action
from rest_framework import permissions

from . import models
from . import serializers
from . import filters as custom_filters
from . import ordering as custom_ordering
from . import permissions as custom_permissions


class TagViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    pagination_class = None
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (custom_permissions.IsAdminOrReadOnly,)
    http_method_names = ('get', 'post')
    lookup_field = 'slug'


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = serializers.FollowSerializer
    permission_classes = (custom_permissions.IsOwnerOrReadOnly,
                          permissions.IsAuthenticated)
    lookup_field = 'author__username'

    def get_queryset(self):
        return models.Follow.objects.filter(user=self.request.user)


class FavoritesViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = serializers.FavoritesSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'recipe__slug'

    def get_queryset(self):
        return models.Favorites.objects.filter(user=self.request.user)
