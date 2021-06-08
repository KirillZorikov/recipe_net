from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from . import models
from . import serializers
from . import utils
from . import filters as custom_filters
from . import permissions as custom_permissions
from .models import User


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


class PurchaseViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    pagination_class = None
    serializer_class = serializers.PurchaseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'recipe__slug'

    def get_queryset(self):
        return models.Purchase.objects.filter(user=self.request.user)

    @action(detail=False, methods=('get',))
    def download(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # if not queryset.exists():
        #     return HttpResponse(status=404)
        filename = 'purchases.txt'
        purchases = utils.make_purchases(self.request.user.username)
        response = HttpResponse(purchases,
                                content_type='text/plain; charset=UTF-8')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


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
        """Return recipes from favorites."""
        return self.list(self, request, *args, **kwargs)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def purchases(self, request, *args, **kwargs):
        """Return recipes from purchase list."""
        return self.list(self, request, *args, **kwargs)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=serializers.FollowRecipesSerializer,
        filter_class=None
    )
    def follows(self, request, *args, **kwargs):
        """Return following's recipes."""
        return self.list(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = models.Recipe.objects.annotate_additional_fields(
            self.request.user
        )
        if self.action == 'follow':
            return User.objects.filter(following__user=self.request.user
                                       ).prefetch_related('recipes')
        if self.action == 'favorites':
            return queryset.filter(author__favorites__user=self.request.user)
        if self.action == 'purchase':
            return queryset.filter(author__purchase__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AuthorRecipesViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = custom_filters.RecipeFilter
    http_method_names = ('get',)

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs['username'])
        return models.Recipe.objects.filter(
            author=author
        ).annotate_additional_fields(self.request.user)
