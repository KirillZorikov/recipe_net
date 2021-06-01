from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Ingredient, Tag, Recipe, Unit, Product

for model in [Unit, Product, Ingredient]:
    admin.site.register(model)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author', 'description', 'get_image')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author', 'tags')
    readonly_fields = ('get_image',)
    fields = ('title', 'author', 'description',
              'ingredients', 'tags', 'time',
              'image', 'get_image')
    save_on_top = True
    save_as = True
    list_per_page = 30
    empty_value_display = '-empty-'

    def get_image(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="50">'
            )
        return '-empty-'

    get_image.short_description = 'Thumbnail'
