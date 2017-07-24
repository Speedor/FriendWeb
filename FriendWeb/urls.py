# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin
from Index.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 默认首页
    url(r'^$', index),
    # ============================================== 用户中心
    # 注册用的路由定义
    url(r'reg/$', register),
    # 登入用的路由定义
    url(r'login/$', log_in),
    # 退出用的路由定义
    url(r'logout/$', log_out),
    # ============================================== 管理中心
    # 管理中心路由
    url(r'manage/$', manage),
    # ============================================== 分类路由
    # 添加博文分类路由
    url(r'^add_sort/$', add_sort),
    # 编辑博文分类路由
    url(r'^edit_sort/$', edit_sort),
    # 删除博文分类路由
    url(r'^del_sort/$', del_sort),
    # ============================================== 博文路由
    # 添加博文
    url(r'^add_blog/$', add_blog),
    # 图片接收路由
    url(r'upload/$', upload),
    # 博客详情
    url(r'^detail_blog/$', detail_blog),
    # 编辑博客
    url(r'^edit_blog/$', edit_blog),
    # 删除博客
    url(r'^del_blog/$', del_blog),
    # handlerbars 用的接口
    # url(r'^index_api/$', index_api),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
