import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_recipe_net_settings_.settings')

app = Celery('recipe_net')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'api.api_user.tasks.inform_admins',
        'schedule': crontab(minute=0, hour=0),
    },
}