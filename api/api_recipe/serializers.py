from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import json

from .models import (User,
                     Product,
                     Tag,
                     Recipe,
                     Unit,
                     Ingredient,
                     Follow,
                     Favorites)


class TagRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {'title': value.title, 'slug': value.slug}

    def to_internal_value(self, data):
        try:
            tag = Tag.objects.get(slug=data)
        except ValueError:
            raise ValidationError()
        return tag


class IngredientRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {'title': value.product.title,
                'unit': value.product.unit.title,
                'quantity': value.quantity}

    def to_internal_value(self, data):
        try:
            data = json.loads(data.replace('\'', '"'))
            unit, _ = Unit.objects.get_or_create(title=data.get('unit'))
            product, _ = Product.objects.get_or_create(
                title=data.get('title'),
                unit=unit
            )
            ingredient, _ = Ingredient.objects.get_or_create(
                product=product,
                quantity=data.get('quantity')
            )
        except ValueError:
            raise ValidationError()
        return ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('slug', 'title')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(queryset=Tag.objects.all(),
                           many=True)
    ingredients = IngredientRelatedField(queryset=Ingredient.objects.all(),
                                         many=True)

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
