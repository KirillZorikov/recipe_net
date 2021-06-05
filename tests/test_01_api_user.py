import glob
import os
import pytest
import re

from django.conf import settings


class TestAPIUser:

    @pytest.mark.django_db(transaction=True)
    def test_01_user_login(self, client, db_user):
        data = {
            'username': 'admin',
            'password': 'admin'
        }
        response = client.post('/api/v1/auth/login', data=data)
        assert response.status_code == 200

    @pytest.mark.django_db(transaction=True)
    def test_02_user_register(self, client, settings_override_recaptcha):
        data = {
            'username': 'tests',
            'password': '123test456',
            'password2': '123test456',
            'email': 'test@ya.ru',
            # official recapthca test key
            'recaptcha_key': '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
        }
        response = client.post('/api/v1/auth/register', data=data)
        assert response.status_code == 201

    @pytest.mark.django_db(transaction=True)
    def test_03_change_password(self, user_client):
        data = {
            'old_password': 'admin',
            'password': '123admin456',
            'password2': '123admin456'
        }
        response = user_client.patch('/api/v1/auth/change_password',
                                     data=data)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('success') == ('Password updated '
                                                'successfully.')

    @pytest.mark.django_db(transaction=True)
    def test_04_reset_password_request(self, user_client,
                                       settings_override_smtp):
        data = {
            'email': 'asa@sds.ru',
        }
        response = user_client.post('/api/v1/auth/reset_password',
                                    data=data)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('success') == 'Instructions sent to email.'

    @pytest.mark.django_db(transaction=True)
    def test_05_reset_password_complete(self, client,
                                        settings_override_smtp, sent_email):
        list_of_files = glob.glob(str(settings.BASE_DIR / 'tests/sent_emails/*'))
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, 'rt') as file:
            email_text = file.read()
        uidb64 = re.search(r'uidb64=(.+)&', email_text).group(1)
        token = re.search(r'token=(.+)', email_text).group(1)
        data = {
            'password': '123adm456',
            'password2': '123adm456'
        }
        url = (f'/api/v1/auth/reset_password_complete'
               f'?uidb64={uidb64}&token={token}')
        response = client.post(url, data=data)
        response_data = response.json()
        assert response.status_code == 200
        assert response_data.get('success') == 'Password changed successfully.'
