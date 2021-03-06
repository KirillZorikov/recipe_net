from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Favorite, Follow, Ingredient, Product, Purchase, Recipe,
                     Tag, Unit)

for model in [Unit, Product, Favorite, Follow, Purchase]:
    admin.site.register(model)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit')
    list_filter = ('product__title',)

    def title(self, obj):
        return obj.product.title

    def unit(self, obj):
        return obj.product.unit


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'description',
                    'slug', 'get_image')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author', 'tags')
    readonly_fields = ('get_image', 'favorites_count')
    fields = ('title', 'author', 'description', 'ingredients',
              'tags', 'time', 'favorites_count',
              'image', 'get_image')
    save_on_top = True
    save_as = True
    list_per_page = 30
    empty_value_display = '-empty-'

    def get_image(self, obj):
        if obj.image:
            link = obj.image.url
            return mark_safe(
                f'<a href="{link}" target="_blank">'
                f'<img src="{link}" width="50">'
                f'</a>'
            )
        return '-empty-'

    def favorites_count(self, obj):
        return obj.favorites.count()

    get_image.short_description = 'Thumbnail'
    favorites_count.short_description = 'Favorites count'
