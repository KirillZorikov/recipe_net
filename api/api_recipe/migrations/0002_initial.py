# Generated by Django 3.2.3 on 2021-06-01 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api_recipe', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(help_text='Recipe author', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Recipe ingredients', to='api_recipe.Ingredient', verbose_name='Ingredients'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Recipe tags', to='api_recipe.Tag', verbose_name='Tag'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='title',
            field=models.ForeignKey(help_text='Product title', on_delete=django.db.models.deletion.CASCADE, to='api_recipe.product', verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unit',
            field=models.ForeignKey(help_text='Product unit', on_delete=django.db.models.deletion.CASCADE, to='api_recipe.unit', verbose_name='Unit'),
        ),
    ]
