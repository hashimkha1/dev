import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coda_project.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coda_project.prod_settings')

app = Celery('coda_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'run_on_every_1st': {
        'task': 'task_history',
        'schedule': crontab(0, 0, day_of_month='1'),
    },
    'login_no_activity_send_sms': {
        'task': 'SendMsgApplicatUser',
        'schedule': crontab(minute='*'),
    },
    'loan_amount_detection': {
        'task': 'TrainingLoanDeduction',
        # 'schedule': crontab(minute='*/1'),
        'schedule': crontab(day_of_month=28),
    },

    'replies_mails': {
        'task': 'replies_job_mail',
        # 'schedule': crontab(minute='*/1'),
        'schedule': crontab(hour=23),
    },

}
