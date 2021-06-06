import pytest


class TestFollow:

    @pytest.mark.django_db(transaction=True)
    def test_01_make_follow(self, user_client, db_user):
        data = {
            'author': 'test',
        }
        follow_list_before = user_client.get('/api/v1/follows').json()
        response = user_client.post('/api/v1/follows', data=data)
        follow_list_after = user_client.get('/api/v1/follows').json()
        assert response.status_code == 201
        assert len(follow_list_before) == len(follow_list_after) - 1

    @pytest.mark.django_db(transaction=True)
    def test_02_make_follow_unauthorized(self, client, db_user):
        data = {
            'author': 'test',
        }
        response = client.post('/api/v1/follows', data=data)
        assert response.status_code == 401

    @pytest.mark.django_db(transaction=True)
    def test_03_make_follow_on_herself(self, user_client, db_user):
        data = {
            'author': 'admin',
        }
        response = user_client.post('/api/v1/follows', data=data)
        response_data = response.json()
        assert response.status_code == 400
        assert (response_data.get('non_field_errors') ==
                ['You can\'t subscribe on herself.'])

    @pytest.mark.django_db(transaction=True)
    def test_04_make_follow_on_non_exist(self, user_client, db_user):
        data = {
            'author': 'non_exist',
        }
        response = user_client.post('/api/v1/follows', data=data)
        response_data = response.json()
        assert response.status_code == 400
        assert response_data.get('author') == [('Object with username='
                                                'non_exist does not exist.')]

    @pytest.mark.django_db(transaction=True)
    def test_05_delete_follow(self, user_client, db_follow):
        username = 'test'
        follow_list_before = user_client.get('/api/v1/follows').json()
        response = user_client.delete(f'/api/v1/follows/{username}')
        follow_list_after = user_client.get('/api/v1/follows').json()
        assert response.status_code == 204
        assert len(follow_list_before) - 1 == len(follow_list_after)

    @pytest.mark.django_db(transaction=True)
    def test_05_delete_non_exist_follow(self, user_client, db_follow):
        username = 'non_exist'
        response = user_client.delete(f'/api/v1/follows/{username}')
        assert response.status_code == 404

    @pytest.mark.django_db(transaction=True)
    def test_06_make_follow_duplicate(self, user_client, db_follow):
        data = {
            'author': 'test',
        }
        response = user_client.post('/api/v1/follows', data=data)
        assert response.status_code == 400
