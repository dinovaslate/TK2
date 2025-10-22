"""WSGI config for tk2project project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tk2project.settings')

application = get_wsgi_application()
