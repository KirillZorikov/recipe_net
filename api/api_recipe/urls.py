from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register(
    'favorites',
    views.FavoritesViewSet,
    basename='favorites',
)
router.register(
    'tags',
    views.TagViewSet,
    basename='tags',
)
router.register(
    'purchases',
    views.PurchaseViewSet,
    basename='purchases',
)
router.register(
    'follows',
    views.FollowViewSet,
    basename='follows',
)
router.register(
    'recipes',
    views.RecipeViewSet,
    basename='recipes',
)
urlpatterns = [
    re_path('v1/', include(router.urls)),
]
