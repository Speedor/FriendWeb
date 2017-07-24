# -*- coding: utf-8 -*-
"""
FriendWeb URL 配置
"""
from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$', ajax_index),

]