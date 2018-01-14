# -*- coding: utf-8 -*-
from django.http import HttpResponse


def health(request):
    """Return a 200 status code when the service is healthy.
    This endpoint returning a 200 means the service is healthy, anything else
    means it is not. It is called frequently and should be fast.
    """
    return HttpResponse('')


def index(request):
    return HttpResponse('')
