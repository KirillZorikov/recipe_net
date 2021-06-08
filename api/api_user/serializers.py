from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .mixins import RecaptchaValidationMixin
from .models import User
from api.api_recipe.models import Follow


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=150, write_only=True)
    username = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(required=False)

    def validate(self, data):
        if not data.get('username') and not data.get('email'):
            raise serializers.ValidationError({'login': 'You should enter '
                                                        'username or email.'})
        return data


class AuthUserSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()
    refresh_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'access_token',
                  'refresh_token')
        read_only_fields = ('id', 'is_active', 'is_staff', 'access_token',
                            'refresh_token')

    def get_access_token(self, instance):
        return str(AccessToken.for_user(user=instance))

    def get_refresh_token(self, instance):
        return str(RefreshToken.for_user(user=instance))


class UserRegisterSerializer(serializers.ModelSerializer,
                             RecaptchaValidationMixin):
    recaptcha_key = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email',
                  'password', 'recaptcha_key',
                  'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didn\'t match.'}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('recaptcha_key')
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didn\'t match.'}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {'old_password': 'Old password is not correct'}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ResetUserPasswordSerializer(serializers.Serializer):
    email = serializers.SlugRelatedField(slug_field='email',
                                         queryset=User.objects.all())

    def validate_email(self, value):
        user = self.context['request'].user
        if user.is_authenticated and value.email != user.email:
            raise serializers.ValidationError(
                {'email': 'Email is not correct'}
            )
        return value


class ResetPasswordCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=150, write_only=True)
    password2 = serializers.CharField(max_length=150, write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didn\'t match.'}
            )
        return attrs


class UserInfoSerializer(serializers.ModelSerializer):
    do_follow = serializers.SerializerMethodField()
    name = serializers.CharField(source='first_name')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'do_follow')

    def get_do_follow(self, instance):
        user = self.context['request'].user
        return user.is_authenticated and Follow.objects.filter(
            author=instance, user=user
        ).exists()
