
from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
CSRF_TRUSTED_ORIGINS = ['https://bodolatest-production.up.railway.app']

DATABASES = {
    "default": {
     'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'vusV9jolYSmAzdUwG9gs',
        'HOST': 'containers-us-west-133.railway.app',
        'PORT': '7687',
    },
}
django_heroku.settings(locals())
