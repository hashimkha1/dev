web: gunicorn coda_project.wsgi
worker: python chrome.py
worker: celery -A coda_project worker --beat --loglevel=DEBUG