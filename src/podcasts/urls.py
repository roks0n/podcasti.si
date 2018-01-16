# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from podcasts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health),
    path('', views.IndexView.as_view(), name='index'),
    path(
        '<slug:podcast_slug>/ep/<slug:episode_slug>/',
        views.EpisodeView.as_view(),
        name='episode'
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
