web: gunicorn coda_project.wsgi:application
worker: celery -A coda_project worker --beat --loglevel=DEBUG