from .base import *

SECRETS = SECRETS_FULL['dev_hj']

DEBUG = True
WSGI_APPLICATION = 'config.wsgi.dev_hj.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS += []

INSTALLED_APPS += []
