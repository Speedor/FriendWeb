# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# 博文分类表
class SortTable(models.Model):
    id = models.AutoField(primary_key=True)
    sort_name = models.CharField(max_length=30)


# 上传图片资源表
class PicTable(models.Model):
    id = models.AutoField(primary_key=True)
    pic = models.FileField(upload_to='blog/')


# 博文记录表
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name=u'标题')
    content = models.TextField(verbose_name='内容')
    pic = models.ForeignKey(PicTable)
    user = models.ForeignKey(User, verbose_name='作者')
    sort = models.ForeignKey(SortTable, verbose_name='分类')
