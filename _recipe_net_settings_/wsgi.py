import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_recipe_net_settings_.settings')

application = get_wsgi_application()
