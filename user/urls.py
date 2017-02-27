#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url
from . import views, user_info

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', user_info.index),
]
