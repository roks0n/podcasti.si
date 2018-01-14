# -*- coding: utf-8 -*-

"""
WSGI config for podcasts.
"""

from django.core.wsgi import get_wsgi_application

from whitenoise.django import DjangoWhiteNoise


def get_application():
    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)
    return application
