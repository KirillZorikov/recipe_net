from rest_framework import serializers
from rest_framework.exceptions import ValidationError

import json

from . import models


class TagRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {'title': value.title, 'slug': value.slug}

    def to_internal_value(self, data):
        try:
            tag = models.Tag.objects.get(slug=data)
        except ValueError:
            raise ValidationError()
        return tag


class AuthorRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {'username': value.username, 'name': value.first_name}

    def to_internal_value(self, data):
        try:
            author = models.User.objects.get(username=data)
        except ValueError:
            raise ValidationError()
        return author


class IngredientRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {'title': value.product.title,
                'unit': value.product.unit.title,
                'quantity': value.quantity}

    def to_internal_value(self, data):
        try:
            data = json.loads(data.replace('\'', '"'))
            unit, _ = models.Unit.objects.get_or_create(title=data.get('unit'))
            product, _ = models.Product.objects.get_or_create(
                title=data.get('title'),
                unit=unit
            )
            ingredient, _ = models.Ingredient.objects.get_or_create(
                product=product,
                quantity=data.get('quantity')
            )
        except ValueError:
            raise ValidationError()
        return ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('slug', 'title')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(
        queryset=models.Tag.objects.all(),
        many=True
    )
    author = AuthorRelatedField(
        queryset=models.User.objects.all(),
        required=False
    )
    ingredients = IngredientRelatedField(
        queryset=models.Ingredient.objects.all(),
        many=True
    )
    in_favorites = serializers.BooleanField(read_only=True)
    do_follow = serializers.BooleanField(read_only=True)
    in_purchase = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Recipe
        fields = ('title',
                  'author',
                  'image',
                  'description',
                  'ingredients',
                  'tags',
                  'time',
                  'slug',
                  'in_favorites',
                  'do_follow',
                  'in_purchase')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=models.User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=models.User.objects.all(),
    )

    def validate(self, data):
        if data['author'] == data['user']:
            raise serializers.ValidationError('You can\'t subscribe '
                                              'on herself.')
        return data

    class Meta:
        fields = ('user', 'author')
        model = models.Follow


class FavoritesSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=models.User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    recipe = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Recipe.objects.all(),
    )

    def validate(self, data):
        """django doesn't do this check itself for favorite and crashes if
        not done, but the follow works well. miracle."""
        if models.Favorites.objects.filter(user=data['user'],
                                           recipe_id=data['recipe']).exists():
            raise serializers.ValidationError('Duplicate favorites.')
        return data

    class Meta:
        fields = ('user', 'recipe')
        model = models.Favorites


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=models.User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    recipe = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.Recipe.objects.all(),
    )

    def validate(self, data):
        if models.Purchase.objects.filter(user=data['user'],
                                          recipe_id=data['recipe']).exists():
            raise serializers.ValidationError('Duplicate purchase.')
        return data

    class Meta:
        fields = ('user', 'recipe')
        model = models.Purchase


class FollowRecipesSerializer(serializers.ModelSerializer):
    recipes = RecipeSerializer(many=True, read_only=True)
    name = serializers.CharField(source='first_name')

    class Meta:
        fields = ('username', 'name', 'recipes')
        model = models.User


class ProductSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(source='unit.title')

    class Meta:
        fields = ('title', 'unit')
        model = models.Product