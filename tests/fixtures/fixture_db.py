import pytest
from django.core.management import call_command

from pytest_django.fixtures import _django_db_fixture_helper


@pytest.fixture
def db_user(request, django_db_setup, django_db_blocker):
    _django_db_fixture_helper(request, django_db_blocker)
    call_command('loaddata', 'tests/tests_data/user.json')


@pytest.fixture
def sent_email(client, admin, settings_override_smtp):
    data = {
        'email': admin.email,
    }
    client.post('/api/v1/auth/reset_password',
                data=data)
