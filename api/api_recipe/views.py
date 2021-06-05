from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework import permissions

from . import models
from . import serializers
from . import filters as custom_filters
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
    permission_classes = (permissions.IsAuthenticated,)
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


class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_class = custom_filters.RecipeFilter
    permission_classes = (custom_permissions.IsOwnerOrReadOnly,)
    serializer_class = serializers.RecipeSerializer
    lookup_field = 'slug'

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorites(self, request, *args, **kwargs):
        """Return all recipes from favorites."""
        return self.list(self, request, *args, **kwargs)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def follow(self, request, *args, **kwargs):
        """Return all following's recipes."""
        return self.list(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = models.Recipe.objects.all()
        if self.action == 'follow':
            return queryset.filter(author__following__user=self.request.user)
        if self.action == 'favorites':
            return queryset.filter(author__favorites__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
