"""
WSGI config for podcasts.
"""

from django.core.wsgi import get_wsgi_application


def get_application():
    application = get_wsgi_application()
    return application
