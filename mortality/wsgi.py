"""
WSGI config for mortality project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/mortality_visualized')
sys.path.append('/var/www/mortality_visualized/mortality/')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mortality.settings')

application = get_wsgi_application()
