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
