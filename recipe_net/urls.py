from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path

from api.api_recipe import urls as recipe_urls
from api.api_user import urls as user_urls

urlpatterns = [
    re_path('admin_panel/', admin.site.urls),
    re_path('api/', include(user_urls)),
    re_path('api/', include(recipe_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
