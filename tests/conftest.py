import pytest

pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_db',
    'tests.fixtures.fixture_settings',
]


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
