# -*- coding: utf-8 -*-

from django.shortcuts import render


# ajax 首页
def ajax_index(request):
    return render(request, 'ajax_blog/index.html')