from django.urls import include, re_path
from rest_framework import routers

from .views import AuthViewSet, UserInfo

router = routers.DefaultRouter(trailing_slash=False)
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserInfo, basename='user_info')

urlpatterns = [
    re_path('v1/', include(router.urls)),
]
