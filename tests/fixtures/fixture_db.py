import pytest
from django.conf import settings
from django.core.management import call_command
from pytest_django.fixtures import _django_db_fixture_helper


@pytest.fixture
def db_user(request, django_db_setup, django_db_blocker):
    _django_db_fixture_helper(request, django_db_blocker)
    call_command('loaddata', settings.BASE_DIR / 'tests/tests_data/user.json')


@pytest.fixture
def db_tag(request, django_db_setup, django_db_blocker):
    _django_db_fixture_helper(request, django_db_blocker)
    call_command('loaddata', settings.BASE_DIR / 'tests/tests_data/tag.json')


@pytest.fixture
def db_ingredient(request, django_db_setup, django_db_blocker):
    _django_db_fixture_helper(request, django_db_blocker)
    call_command('loaddata', settings.BASE_DIR / 'tests/tests_data/unit.json')
    call_command('loaddata', settings.BASE_DIR / 'tests/tests_data/product.json')
    call_command('loaddata', settings.BASE_DIR / 'tests/tests_data/ingredient.json')


@pytest.fixture
def db_recipe(request, django_db_setup, django_db_blocker, db_user, db_ingredient, db_tag):
    _django_db_fixture_helper(request, django_db_blocker)
    call_command('loaddata', settings.BASE_DIR / 'tests/tests_data/recipe.json')


@pytest.fixture
def db_follow(request, django_db_setup, django_db_blocker, db_user):
    _django_db_fixture_helper(request, django_db_blocker)
    call_command('loaddata', settings.BASE_DIR / 'tests/tests_data/follow.json')


@pytest.fixture
def db_favorites(request, django_db_setup, django_db_blocker, db_recipe):
    _django_db_fixture_helper(request, django_db_blocker)
    call_command('loaddata', settings.BASE_DIR / 'tests/tests_data/favorites.json')


@pytest.fixture
def sent_email(client, settings_override_smtp):
    data = {
        'email': 'asa@sds.ru',
    }
    client.post('/api/v1/auth/reset_password',
                data=data)
