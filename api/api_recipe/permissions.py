from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


IsAdminOrReadOnly = ReadOnly | (IsAuthenticated & IsAdmin)
IsOwnerOrReadOnly = ReadOnly | (IsAuthenticated & IsOwner)
IsOwnerOrReadOnlyOrAdmin = IsAdminOrReadOnly | IsOwnerOrReadOnly
