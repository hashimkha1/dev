from coda_project.setting.base import *
# SECURITY
SECRET_KEY = "!cxl7yhjsl00964n=#e-=xblp4u!hbajo2k8u#$v9&s6__5=xf"

DEBUG = True
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'CODA_UAT',# Name of Database
#         'USER':'postgres',
#         'PASSWORD': os.environ.get('POSTGRESSPASS'),
#         'HOST': 'localhost',
#     }
# }

# coda\coda_project\settings\development.py

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'CODA_UAT',# Name of Database
#         'USER':'postgres',
#         'PASSWORD': 'MANAGER2030', #os.environ.get('POSTGRESSPASS'),
#         'HOST': 'localhost',
#     }
# }
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }

import dj_database_url
# postgresql database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "testing",  # Name of Database
        "USER": "postgres",
        "PASSWORD": "Honnappa001@500",  # os.environ.get('POSTGRESSPASS'),
        "HOST": "localhost",
    }
}
db_from_env = dj_database_url.config(conn_max_age=600)

# Gmail Email Backend Account
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com" 
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("EMAIL_USER") 
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASS") 

SITEURL="http://localhost:8000"