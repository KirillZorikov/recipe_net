import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


class TestRecipe:

    @pytest.mark.django_db(transaction=True)
    def test_01_get_recipes_list(self, client, db_recipe):
        response = client.get('/api/v1/recipes')
        resource_data = response.json()['response']
        assert response.status_code == 200
        assert len(resource_data) == 2

    @pytest.mark.django_db(transaction=True)
    def test_02_get_recipe_by_slug(self, client, db_recipe):
        slug = '2-yabloko-s-myodom'
        response = client.get(f'/api/v1/recipes/{slug}')
        resource_data = response.json()
        assert response.status_code == 200
        assert resource_data.get('slug') == slug

    @pytest.mark.django_db(transaction=True)
    def test_03_get_favorite_recipes(self, user_client,
                                     db_favorites, db_recipe):
        response = user_client.get(f'/api/v1/recipes/favorites')
        resource_data = response.json()['response']
        assert response.status_code == 200
        assert len(resource_data) == 1

    @pytest.mark.django_db(transaction=True)
    def test_04_get_following_recipes(self, user_client,
                                      db_follow, db_recipe):
        response = user_client.get(f'/api/v1/recipes/follows')
        resource_data = response.json()['response']
        assert response.status_code == 200
        assert len(resource_data) == 1

    @pytest.mark.django_db(transaction=True)
    def test_04_create_recipe(self, user_client, db_user,
                              db_ingredient, db_tag):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        image_data = SimpleUploadedFile('small.gif', small_gif,
                                        content_type='image/gif')
        data = {
            'title': 'яблоко с мёдом',
            'author': 'admin',
            'image': image_data,
            'description': 'пойдёт',
            'time': 5,
            'ingredients': [{'title': 'яблоки', 'unit': 'г', 'quantity': 20}],
            'tags': ['obed', 'zavtrak']
        }
        recipes_before = user_client.get('/api/v1/recipes').json()['response']
        response = user_client.post('/api/v1/recipes', data=data)
        resource_data = response.json()
        recipes_after = user_client.get('/api/v1/recipes').json()['response']
        assert response.status_code == 201
        assert resource_data.get('title') == data['title']
        assert len(recipes_before) == len(recipes_after) - 1
