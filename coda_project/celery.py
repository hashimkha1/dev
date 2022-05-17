
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coda_project.settings')


BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
DEBUG = 1
app = Celery('coda_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_url = BASE_REDIS_URL

# app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'


app.conf.beat_schedule = {
    'add-every-10-seconds': {
        'task': 'task_history',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),
    },
}