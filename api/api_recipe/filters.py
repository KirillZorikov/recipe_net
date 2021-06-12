import django_filters

from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__slug', method='filter_tags')

    class Meta:
        model = Recipe
        fields = ('tags',)

    def filter_tags(self, queryset, field_name, tags):
        tags = tags.split(',')
        return queryset.filter(tags__slug__in=tags).distinct()
