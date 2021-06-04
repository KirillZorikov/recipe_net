import django_filters

from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(field_name='tags__slug', method='filter_tag')

    class Meta:
        model = Recipe
        fields = ('tags', )

    def filter_tag(self, queryset, field_name, tag):
        return queryset.filter(tags__slug=tag)

