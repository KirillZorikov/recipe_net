from django.urls import re_path, include
from rest_framework import routers

from .views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = [
    re_path('v1/', include(router.urls)),
]