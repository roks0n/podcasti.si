# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from podcasts import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^health/', views.health),
    url(r'^$', views.IndexView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
