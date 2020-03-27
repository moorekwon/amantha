from .base import *

SECRETS = SECRETS_FULL['production']

DEBUG = False
WSGI_APPLICATION = 'config.wsgi.production.application'

DATABASES = SECRETS['DATABASES']

ALLOWED_HOSTS += ['*']
INSTALLED_APPS += []
