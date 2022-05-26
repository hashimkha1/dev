
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coda_project.settings')

app = Celery('coda_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'run_on_every_1st': {
        'task': 'task_history',
        'schedule': crontab(0, 0, day_of_month='1'),
    },
}
