# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import TemplateView


def health(request):
    """Return a 200 status code when the service is healthy.
    This endpoint returning a 200 means the service is healthy, anything else
    means it is not. It is called frequently and should be fast.
    """
    return HttpResponse('')


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'header': {
                'url': 'example.com',
                'title': 'Slovenski Podcasti',
                'subtitle': 'Seznam vseh slovenskih podcastov'
            },
        })
        return context
