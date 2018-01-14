# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

from podcasts import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^health/', views.health),
    url(r'^$', views.index),
]
