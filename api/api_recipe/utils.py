from django.db.models import F, Sum

from . import models


def make_purchases(username):
    result_txt = ''
    ingredients = models.Ingredient.objects.filter(
        recipes__purchase__user__username=username
    ).annotate(
        title=F('product__title')
    ).annotate(
        unit=F('product__unit__title')
    ).values('title', 'unit').annotate(quantity=Sum('quantity'))
    for ingredient in ingredients:
        result_txt += (f'{ingredient["title"]} '
                       f'({ingredient["unit"]}) - '
                       f'{ingredient["quantity"]} \n')
    return result_txt
