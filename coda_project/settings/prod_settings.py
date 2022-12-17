import os
from pickle import TRUE

import django_heroku
import redis

DEBUG = False

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


# #postgresql database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'CODA_UAT',# Name of Database
#         'USER':'postgres',
#         'PASSWORD': 'MANAGER#2030', #os.environ.get('POSTGRESSPASS'),
#         'HOST': 'localhost',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'CODADB_DEV',# Name of Database
#         'USER':'postgres',
#         'PASSWORD': os.environ.get('POSTGRESSPASS'),
#         'HOST': 'localhost',
#     }
# }

import dj_database_url
# #postgresql database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'CODA_DEV',# Name of Database
#         'USER':'CODA_DEV',
#         'PASSWORD': os.environ.get('POSTGRESSPASS'),
#         'HOST': 'database-1.ckq8mwyj2m9n.us-east-2.rds.amazonaws.com',
#         'PORT': '5432'
#     }
# }

db_from_env = dj_database_url.config(conn_max_age=600)

DATABASES["default"].update(db_from_env)












# Email Backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.privateemail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")  # "info@codanalytics.net"
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASS")
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER




# ! Make sure the below line of code is not commented on the production for media uploads
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# STATICFILES_STORAGE='storages.backends.s3boto3.S3Boto3Storage'
django_heroku.settings(locals())



SITEURL="https://www.codanalytics.net"