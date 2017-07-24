# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# django原生框架首页
def django_index(request):
    return render(request, 'django/index.html')
