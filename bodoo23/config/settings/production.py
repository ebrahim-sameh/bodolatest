
from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
    "ENGINE": "django.db.backends.postgresql",
    'NAME': os.environ.get('QOVERY_POSTGRESQL_Z367580A2_DEFAULT_DATABASE_NAME', 'postgres'),
    'USER': os.environ.get('QOVERY_POSTGRESQL_Z367580A2_LOGIN', 'qoveryadmin'),
    'PASSWORD': os.environ.get('QOVERY_POSTGRESQL_Z367580A2_PASSWORD'),
    'HOST': os.environ.get('QOVERY_POSTGRESQL_Z367580A2_HOST', 'z367580a2-postgresql.zeddf7074.criom.sh'),
    'PORT': os.environ.get('QOVERY_POSTGRESQL_Z367580A2_PORT', 5432),
    },
}
django_heroku.settings(locals())
