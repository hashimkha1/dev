web: gunicorn coda_project.wsgi --log-file
worker: celery -A coda_project worker --beat --loglevel=DEBUG