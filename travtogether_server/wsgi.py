"""
WSGI config for travtogether_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from travtogether_server.current_settings import CURRENT_SETTING
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', CURRENT_SETTING)

application = get_wsgi_application()
