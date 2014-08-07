"""
tally settings, FOR TESTING PURPOSES ONLY
(this file is not included in the distribution)
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ALLOWED_HOSTS = ['*']

SECRET_KEY = 'tally_tests_are_not_secret'

INSTALLED_APPS = (
    'tally',
)

ROOT_URLCONF = 'tally.urls'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Required
TALLY_DATA_DIR = os.path.join(BASE_DIR, 'data')
