from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Exists, OuterRef
from pytils.translit import slugify

User = get_user_model()


class ModelQuerySet(models.QuerySet):
    def annotate_additional_fields(self, user):
        return self.annotate(
            in_favorites=Exists(
                Favorite.objects.filter(
                    user=user.id,
                    recipe_id=OuterRef('id')
                ).only('id')
            )
        ).annotate(
            do_follow=Exists(
                Follow.objects.filter(
                    user=user.id,
                    author=OuterRef('author')
                ).only('id')
            )
        ).annotate(
            in_purchase=Exists(
                Purchase.objects.filter(
                    user=user.id,
                    recipe_id=OuterRef('id')
                ).only('id')
            )
        )


class Tag(models.Model):
    """tag for the recipe"""
    title = models.CharField(max_length=50,
                             verbose_name='Title',
                             help_text='Tag title')
    slug = models.SlugField(max_length=50,
                            blank=True,
                            null=True,
                            verbose_name='Slug',
                            help_text='Unique key for url generation')

    class Meta:
        ordering = ('title',)
        get_latest_by = 'id'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Unit(models.Model):
    """product measurement unit"""
    title = models.CharField(max_length=50,
                             verbose_name='Title',
                             help_text='Name of the unit')

    class Meta:
        ordering = ('title',)
        get_latest_by = 'id'
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Title',
                             help_text='Product title')
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name='products',
                             verbose_name='Unit',
                             help_text='Product unit')

    class Meta:
        ordering = ('title',)
        get_latest_by = 'id'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """recipe ingredient"""
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='ingredients',
                                verbose_name='Product',
                                help_text='Product: name + unit')
    quantity = models.PositiveSmallIntegerField(db_index=True,
                                                verbose_name='Quantity',
                                                help_text='Product quantity')

    class Meta:
        ordering = ('product__title',)
        get_latest_by = 'id'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.product.title


class Recipe(models.Model):
    """recipe itself"""
    title = models.CharField(max_length=200,
                             verbose_name='Title',
                             help_text='Recipe title')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Author',
                               help_text='Recipe author')
    image = models.ImageField(upload_to='images/',
                              verbose_name='Image',
                              help_text='Recipe image')
    description = models.CharField(max_length=50000,
                                   verbose_name='Description',
                                   help_text='Recipe description')
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         verbose_name='Ingredients',
                                         help_text='Recipe ingredients')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Tag',
                                  related_name='recipes',
                                  help_text='Recipe tags')
    time = models.PositiveSmallIntegerField(db_index=True,
                                            verbose_name='Time',
                                            help_text='Cooking time(min)')
    slug = models.SlugField(max_length=200,
                            blank=True,
                            null=True,
                            verbose_name='Slug',
                            help_text='Unique key for url generation')

    objects = ModelQuerySet.as_manager()

    class Meta:
        ordering = ('-id',)
        get_latest_by = 'id'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.slug:
            return
        self.slug = slugify(f'{self.pk}-{self.title}')
        self.save()


class Favorite(models.Model):
    """user's favorites list"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='User',
                             help_text='The one who adds to favorites')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorites',
                               verbose_name='Recipe',
                               help_text='Recipe in the favorites')

    class Meta:
        ordering = ('user',)
        get_latest_by = 'id'
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='duplicate_favorites'
            ),
        ]

    def __str__(self):
        return f'{self.user.username}\'s favorites'


class Follow(models.Model):
    """user's follows"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Follower',
                             help_text='The one who makes the follow')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Following',
                               help_text='The one user follow to')

    class Meta:
        ordering = ('user',)
        unique_together = ('user', 'author')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='duplicate_follow'
            ),
        ]

    def __str__(self):
        return f'{self.user.username} follow {self.author.username}'


class Purchase(models.Model):
    """user's purchase"""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='purchase',
                             verbose_name='User',
                             help_text='The one who adds to purchase list')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='purchase',
                               verbose_name='Recipe',
                               help_text='Recipe in the purchase list')

    class Meta:
        ordering = ('user',)
        get_latest_by = 'id'
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='duplicate_purchase'
            ),
        ]

    def __str__(self):
        return f'{self.user.username} add {self.recipe.title} to purchase list'
