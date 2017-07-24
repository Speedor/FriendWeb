# -*- coding: utf-8 -*-
"""
FriendWeb URL 配置
"""
from django.conf.urls import url
from .views import *

# TODO 编辑权限，历史选择，能显示，但没有计算出数据

urlpatterns = [

    url(r'^$', admin_index),

    url(r'^user/$', admin_user),

    url(r'^add_usergroup/$', admin_usergroup_add),

    url(r'^list_usergroup/$', list_usergroup),

    url(r'^edit_usergroup/$', edit_usergroup),

]
