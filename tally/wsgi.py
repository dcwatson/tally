"""
tally WSGI application, FOR TESTING PURPOSES ONLY
(this file is not included in the distribution)
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tally.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
