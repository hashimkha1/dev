"""
Django settings for coda_project project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY ='!cxl7yhjsl00964n=#e-=xblp4u!hbajo2k8u#$v9&s6__5=xf'
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG =(os.environ.get('DEBUG_VALUE')=='True')

ALLOWED_HOSTS = ['codatrainingapp.herokuapp.com']
#ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'users.apps.UsersConfig',
    'codablog.apps.CodablogConfig',
    'data.apps.DataConfig',
    'application.apps.ApplicationConfig',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'coda_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'coda_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'CODADB',# Name of Database
        'USER':'postgres',
        'PASSWORD': 'MANAGER2020', #os.environ.get('POSTGRESSPASS'),
        'HOST': 'localhost',
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        
    }
}
'''


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'
STATICFILES_DIR=(
    os.path.join(BASE_DIR,"static")
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'main-home'
LOGIN_URL = 'user-login'

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=os.environ.get('EMAIL_USER')
EMAIL_HOST_PASS=os.environ.get('EMAIL_PASS')


AWS_S3_REGION_NAME = 'us-east-2' #change to your region
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None
'''
AWS_S3_REGION_NAME = 'us-east-2' #change to your region
#AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_ACCESS_KEY_ID = 'AKIA4WQYAE7ALNTUMN2F'
AWS_SECRET_ACCESS_KEY = 'qU6lpbQZZ3nbhmm8LEPw1EQ3Qn+CmaoFr8fGJWC5'
AWS_STORAGE_BUCKET_NAME = 'coachofanalytics'
AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None
'''

DEFAULT_FILE_STORAGE='storages.backends.s3boto3.S3Boto3Storage'
#STATICFILES_STORAGE='storages.backends.s3boto3.S3Boto3Storage'
django_heroku.settings(locals())