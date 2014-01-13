"""
tally settings, FOR TESTING PURPOSES ONLY
(this file is not included in the distribution)
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '5cqoxo+_f4l=9s3506bxl)7ic4vg2)wg$unz10zktoy(yfuo)m'

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tally',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tally.urls'
WSGI_APPLICATION = 'tally.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tally.db'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'tally': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Required
TALLY_DATA_DIR = os.path.join(BASE_DIR, 'data')

# Optional
TALLY_HOST = '127.0.0.1'
TALLY_PORT = 8900
TALLY_FLUSH_TIME = 5.0
TALLY_INSTALL_ADMIN = True
