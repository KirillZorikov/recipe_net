import pytest


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
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access_admin"]}')
    return client


@pytest.fixture
def not_admin_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {token["access_not_admin"]}'
    )
    return client
