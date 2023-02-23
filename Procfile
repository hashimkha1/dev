web: gunicorn coda_project.wsgi
web: python getdata.utils.py
worker: celery -A coda_project worker --beat --loglevel=DEBUG