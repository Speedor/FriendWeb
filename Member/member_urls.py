# -*- coding: utf-8 -*-
"""
FriendWeb URL 配置
"""
from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$', member_index),

    url(r'^reg/$', member_reg),

    url(r'^login/$', member_login),

    url(r'^logout/$', member_logout),
]