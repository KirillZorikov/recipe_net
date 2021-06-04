from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (User,
                     Product,
                     Tag,
                     Recipe,
                     Unit,
                     Ingredient,
                     Follow,
                     Favorites)


class ProductRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {'title': value.title, 'unit': value.unit.title}

    def to_internal_value(self, data):
        try:
            unit, _ = Unit.objects.get_or_create(title=data['unit'])
            product, _ = Product.objects.get_or_create(title=data['title'],
                                                       unit=unit)
        except ValueError:
            raise ValidationError()
        return product


class IngredientSerializer(serializers.ModelSerializer):
    product = ProductRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Ingredient
        fields = ('product', 'quantity')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('slug', 'title')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('title',
                  'author',
                  'image',
                  'description',
                  'ingredients',
                  'tags',
                  'time',
                  'slug')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    def validate(self, data):
        if data['author'] == data['user']:
            raise serializers.ValidationError('You can\'t subscribe '
                                              'on herself.')
        return data

    class Meta:
        fields = ('user', 'author')
        model = Follow


class FavoritesSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        """django doesn't do this check itself for favorite and crashes if
        not done, but the follow works well. miracle."""
        if Favorites.objects.filter(user=data['user'],
                                    recipe_id=data['recipe']).exists():
            raise serializers.ValidationError('Duplicate favorites.')
        return data

    class Meta:
        fields = ('user', 'recipe')
        model = Favorites
