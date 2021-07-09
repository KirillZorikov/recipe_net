import pytest

from rest_framework.test import APIClient
from django.conf import settings

class CustomAPIClient(APIClient):
    ADDITIONAL_TO_PATH = f'/{settings.PROJECT_NAME}'

    def get(self, path, *args, **kwargs):
       return super().get(self.ADDITIONAL_TO_PATH + path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return super().post(self.ADDITIONAL_TO_PATH + path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return super().put(self.ADDITIONAL_TO_PATH + path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return super().patch(self.ADDITIONAL_TO_PATH + path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return super().delete(self.ADDITIONAL_TO_PATH + path, *args, **kwargs)




@pytest.fixture
def token(db_user, django_user_model):
    from rest_framework_simplejwt.tokens import RefreshToken
    admin = django_user_model.objects.get(username='admin')
    refresh = RefreshToken.for_user(admin)
    not_admin = django_user_model.objects.get(username='test')
    refresh_not_admin = RefreshToken.for_user(not_admin)
    return {
        'access_admin': str(refresh.access_token),
        'access_not_admin': str(refresh_not_admin.access_token)
    }


@pytest.fixture
def client(token):
    return CustomAPIClient()


@pytest.fixture
def user_client(token):
    client = CustomAPIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access_admin"]}')
    return client


@pytest.fixture
def not_admin_client(token):
    client = CustomAPIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {token["access_not_admin"]}'
    )
    return client
