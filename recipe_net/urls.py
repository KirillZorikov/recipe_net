from django.contrib import admin
from django.urls import include, re_path
from django.conf.urls.static import static
from django.conf import settings

from api.api_user import urls as user_urls

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('api/', include(user_urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
