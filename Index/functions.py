# -*- coding: utf-8 -*-
import json
from django.shortcuts import HttpResponse


class MyPermission():
    @staticmethod
    def read_permission(str):
        _arr = str.split(',')
        _result = 0
        for p in _arr:
            _result = _result+pow(2,int(p))
            print '当前选项值:',p,'当前权限值:',_result
        return _result


class MyResponse():
    @staticmethod
    def SendData(object):
        _str = json.dumps(object)
        return HttpResponse(_str, content_type='application/json')