# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


#用户权限表
class UserPermission(models.Model):
    id = models.AutoField(primary_key=True)
    info = models.CharField(max_length=120)

    def __unicode__(self):
        return self.info

#用户编组表
class UserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    permission = models.IntegerField()


#用户表
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    group = models.ForeignKey(UserGroup)


