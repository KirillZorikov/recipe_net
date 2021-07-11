from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

User = get_user_model()


def authenticate_user(password, username=None, email=None):
    user = authenticate(username=username or email, password=password)
    if user is None:
        raise serializers.ValidationError('Invalid data. '
                                          'Please try again!')
    return user


def generate_uidb64_and_token(user, email):
    if user.is_anonymous:
        user = User.objects.get(email=email)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return uidb64, token


def check_token(user, token):
    return default_token_generator.check_token(user, token)
