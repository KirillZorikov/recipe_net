from django.contrib.auth import logout
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import User
from .utils import (authenticate_user,
                    send_instructions,
                    generate_uidb64_and_token,
                    check_token,
                    get_user_by_uidb64)


class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer,
        'change_password': serializers.ChangeUserPasswordSerializer,
        'reset_password': serializers.ResetUserPasswordSerializer,
        'reset_password_complete': serializers.ResetPasswordCompleteSerializer,
    }
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=('post',), permission_classes=(AllowAny,))
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',))
    def logout(self, request):
        logout(request)
        return Response({'success': 'Successfully logged out'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), permission_classes=(AllowAny,))
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=('patch',))
    def change_password(self, request):
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Password updated successfully.'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), permission_classes=(AllowAny,))
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        uidb64, token = generate_uidb64_and_token(request.user, email)
        url = f'{request.build_absolute_uri()}?uidb64={uidb64}&token={token}'
        send_instructions(email, url)
        return Response({'success': 'Instructions sent to email.'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=('post',), permission_classes=(AllowAny,))
    def reset_password_complete(self, request):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = self.request.GET.get('uidb64')
        token =self.request.GET.get('token')
        user = get_user_by_uidb64(uidb64)
        if not user or not check_token(user, token):
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.set_password(request.data['password'])
        user.save()
        return Response({'success': 'Password changed successfully.'},
                        status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
