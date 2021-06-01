from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify

User = get_user_model()


class Tag(models.Model):
    """tag for the recipe"""
    title = models.CharField(max_length=50,
                             verbose_name='Title',
                             help_text='Tag title')
    slug = models.SlugField(max_length=50,
                            verbose_name='Slug',
                            help_text='Unique key for url generation')

    class Meta:
        ordering = ('title',)
        get_latest_by = 'id'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Title',
                             help_text='Product title')

    def __str__(self):
        return self.title


class Unit(models.Model):
    """product measurement unit"""
    title = models.CharField(max_length=50,
                             verbose_name='Title',
                             help_text='Name of the unit')

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    """recipe ingredient"""
    title = models.ForeignKey(Product,
                              on_delete=models.CASCADE,
                              verbose_name='Title',
                              help_text='Product title')
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             verbose_name='Unit',
                             help_text='Product unit')
    quantity = models.PositiveSmallIntegerField(db_index=True,
                                                verbose_name='Quantity',
                                                help_text='Product quantity')

    class Meta:
        ordering = ('title',)
        get_latest_by = 'id'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.title.title


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
    description = models.CharField(max_length=5000,
                                   verbose_name='Description',
                                   help_text='Recipe description')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ingredients',
                                         help_text='Recipe ingredients')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Tag',
                                  help_text='Recipe tags')
    time = models.PositiveSmallIntegerField(db_index=True,
                                            verbose_name='Time',
                                            help_text='Cooking time(min)')
    slug = models.SlugField(max_length=200,
                            blank=True,
                            null=True,
                            verbose_name='Slug',
                            help_text='Unique key for url generation')

    class Meta:
        ordering = ('title', 'author')
        get_latest_by = 'id'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        super(Recipe, self).save(*args, **kwargs)
        if self.slug:
            return
        self.slug = slugify(f'{self.pk}-{self.title}')
        self.save()

