from os import environ
import dj_database_url
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get(
    "SECRET_KEY", "_=PLACEHOLDER=_"
)  # REQUIRED! FOR COLLECT STATIC

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(environ.get("DEBUG", 0))

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "").split(",")


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASE_URI = environ.get("DATABASE_URI")
DATABASES = {"default": dj_database_url.parse(DATABASE_URI) if DATABASE_URI else {}}


# Celery
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#configuration
CELERY_BROKER_URL = environ.get("CELERY_BROKER_URI")
CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_TRACK_STARTED = True
