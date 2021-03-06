# Generated by Django 3.2.3 on 2021-06-04 00:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(db_index=True, help_text='Product quantity', verbose_name='Quantity')),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
                'ordering': ('product__title',),
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Tag title', max_length=50, verbose_name='Title')),
                ('slug', models.SlugField(help_text='Unique key for url generation', verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ('title',),
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Name of the unit', max_length=50, verbose_name='Title')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Recipe title', max_length=200, verbose_name='Title')),
                ('image', models.ImageField(help_text='Recipe image', upload_to='images/', verbose_name='Image')),
                ('description', models.CharField(help_text='Recipe description', max_length=5000, verbose_name='Description')),
                ('time', models.PositiveSmallIntegerField(db_index=True, help_text='Cooking time(min)', verbose_name='Time')),
                ('slug', models.SlugField(blank=True, help_text='Unique key for url generation', max_length=200, null=True, verbose_name='Slug')),
                ('author', models.ForeignKey(help_text='Recipe author', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('ingredients', models.ManyToManyField(help_text='Recipe ingredients', to='api_recipe.Ingredient', verbose_name='Ingredients')),
                ('tags', models.ManyToManyField(help_text='Recipe tags', to='api_recipe.Tag', verbose_name='Tag')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ('title', 'author'),
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Product title', max_length=100, verbose_name='Title')),
                ('unit', models.ForeignKey(help_text='Product unit', on_delete=django.db.models.deletion.CASCADE, to='api_recipe.unit', verbose_name='Unit')),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='product',
            field=models.ForeignKey(help_text='Product: name + unit', on_delete=django.db.models.deletion.CASCADE, to='api_recipe.product', verbose_name='Product'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(help_text='The one user follow to', on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Following')),
                ('user', models.ForeignKey(help_text='The one who makes the follow', on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Follower')),
            ],
            options={
                'verbose_name': 'Follow',
                'verbose_name_plural': 'Follows',
                'ordering': ('user',),
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipes', models.ManyToManyField(help_text='Recipes in the favorites', related_name='favorites', to='api_recipe.Recipe', verbose_name='Recipes')),
                ('user', models.ForeignKey(help_text='The one who adds to favorites', on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Favorites',
                'verbose_name_plural': 'Favorites',
                'ordering': ('user',),
                'get_latest_by': 'id',
            },
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='duplicate_follow'),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'author')},
        ),
    ]
