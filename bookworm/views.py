#!/usr/bin/env python
# encoding: utf-8

from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello django")
