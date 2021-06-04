import pytest


# @pytest.fixture
# def admin(django_user_model):
#     return django_user_model.objects.create_superuser(
#         username='admin', email='admin@yamdb.fake', password='admin'
#     )


@pytest.fixture
def token(db_user, django_user_model):
    from rest_framework_simplejwt.tokens import RefreshToken
    admin = django_user_model.objects.get(username='admin')
    refresh = RefreshToken.for_user(admin)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
def client(token):
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token["access"]}')
    return client
