import pytest


class TestTag:

    @pytest.mark.django_db(transaction=True)
    def test_01_get_tags_list(self, client, db_tag):
        response = client.get('/api/v1/tags')
        resource_data = response.json()
        assert response.status_code == 200
        assert len(resource_data) == 3

    @pytest.mark.django_db(transaction=True)
    def test_02_admin_create_tag(self, user_client, db_tag):
        data = {
            'title': 'new'
        }
        tags_before = user_client.get('/api/v1/tags').json()
        response = user_client.post('/api/v1/tags', data=data)
        tags_after = user_client.get('/api/v1/tags').json()
        assert response.status_code == 201
        assert len(tags_before) == len(tags_after) - 1

    @pytest.mark.django_db(transaction=True)
    def test_03_not_admin_create_tag(self, not_admin_client, db_tag):
        data = {
            'title': 'new'
        }
        response = not_admin_client.post('/api/v1/tags', data=data)
        assert response.status_code == 403
