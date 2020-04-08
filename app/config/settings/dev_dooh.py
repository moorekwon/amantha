from .base import *

SECRETS = SECRETS_FULL['dev']
print(SECRETS)
DEBUG = True
WSGI_APPLICATION = 'config.wsgi.dev_dooh.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS += []

INSTALLED_APPS += []

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'wps-web-clone'
AWS_AUTO_CREATE_BUCKET = True
AWS_S3_REGION_NAME = 'ap-northeast-2'

DATETIME_FORMAT = '%Y-%m-%d %H:%M'
USE_L10N = False
