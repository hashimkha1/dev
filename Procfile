web: gunicorn coda_project.wsgi
web: python chrome.py
worker: celery -A coda_project worker --beat --loglevel=DEBUG