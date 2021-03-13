"""
ASGI config for travtogether_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from travtogether_server.current_settings import CURRENT_SETTING

os.environ.setdefault('DJANGO_SETTINGS_MODULE', CURRENT_SETTING)

application = get_asgi_application()
