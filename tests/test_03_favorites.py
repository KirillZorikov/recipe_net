import pytest


class TestFavorites:

    @pytest.mark.django_db(transaction=True)
    def test_01_add_to_favorites(self, user_client, db_recipe):
        data = {
            'recipe': 1,
        }
        follow_list_before = user_client.get('/api/v1/favorites').json()
        response = user_client.post('/api/v1/favorites', data=data)
        follow_list_after = user_client.get('/api/v1/favorites').json()
        assert response.status_code == 201
        assert len(follow_list_before) == len(follow_list_after) - 1

    @pytest.mark.django_db(transaction=True)
    def test_02_add_to_favorites_unauthorized(self, client, db_user):
        data = {
            'recipe': 1,
        }
        response = client.post('/api/v1/favorites', data=data)
        assert response.status_code == 401

    @pytest.mark.django_db(transaction=True)
    def test_03_add_to_favorites_duplicate(self, user_client, db_favorites):
        data = {
            'recipe': 1,
        }
        response = user_client.post('/api/v1/favorites', data=data)
        response_data = response.json()
        assert response.status_code == 400
        assert (response_data.get('non_field_errors') ==
                ['Duplicate favorites.'])

    @pytest.mark.django_db(transaction=True)
    def test_04_add_to_favorites_non_exist(self, user_client, db_user):
        data = {
            'recipe': 666,
        }
        response = user_client.post('/api/v1/favorites', data=data)
        response_data = response.json()
        assert response.status_code == 400
        assert (response_data.get('recipe') ==
                ['Invalid pk "666" - object does not exist.'])

    @pytest.mark.django_db(transaction=True)
    def test_05_delete_favorites(self, user_client, db_favorites):
        recipe = '1-moloko'
        follow_list_before = user_client.get('/api/v1/favorites').json()
        response = user_client.delete(f'/api/v1/favorites/{recipe}')
        follow_list_after = user_client.get('/api/v1/favorites').json()
        assert response.status_code == 204
        assert len(follow_list_before) - 1 == len(follow_list_after)