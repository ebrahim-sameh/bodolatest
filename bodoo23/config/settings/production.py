
from .base import *

ALLOWED_HOSTS = ['*']

DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "d409iecd7lbjd4",
        "USER":  "ktksnydubidsvm",
        "PASSWORD": "e0512543fc0a6209b84a9ff686f99042f2b2c14e0888fda6e56801439bae0bd4",
        "HOST": "ec2-35-170-146-54.compute-1.amazonaws.com",
        "PORT": 5432,
    },
}
django_heroku.settings(locals())
