import pytest, os
from django.conf import settings


@pytest.fixture
def settings_override_recaptcha(django_user_model):
    # official recapthca test key
    settings.GOOGLE_RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'


@pytest.fixture
def settings_override_smtp(django_user_model):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    settings.EMAIL_FILE_PATH = os.path.join(settings.BASE_DIR,
                                            'tests/sent_emails')
