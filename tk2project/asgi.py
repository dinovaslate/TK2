"""ASGI config for tk2project project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tk2project.settings')

application = get_asgi_application()
