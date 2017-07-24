# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponseRedirect
from .models import *
from .forms import *
from Index.functions import *
from django.db import models

'''
用户表
---------------
注册
登入
修改密码
基本资料修改
绑定手机
绑定邮件
找回密码【邮件、手机】


用户编组表
设置用户编组
编组选项修改


权限配置表
添加权限
删除权限
编辑权限


'''


# 用户中心
def member_index(request):
    return render(request, 'member/member_index.html')


def member_reg(request):
    if request.method == 'POST':
        print('here')
        _form = MemberRegisterForm(request.POST)
        if _form.is_valid():
            print('is_valid')

            _length = User.objects.filter(username=request.POST.get('username')).count()

            if _length == 0:
                _user = _form.cleaned_data['username']
                _pass = _form.cleaned_data['password']
                _email = _form.cleaned_data['email']
                User.objects.create(username=_user, password=_pass, email=_email, group_id=1)
                _statu = {'statu': 1}
            else:
                _statu = {'statu': 0, 'msg': [{'username': u'用户名已经存在'}]}
            return MyResponse.SendData(_statu)

        else:
            _statu = {'statu': 0, 'msg': _form.errors}
            return MyResponse.SendData(_statu)
    return render(request, 'member/member_reg.html')


def member_login(request):
    if request.method == 'POST':
        _form = MemberLoginForm(request.POST)
        if _form.is_valid():
            _user = _form.cleaned_data['username']
            _pass = _form.cleaned_data['password']
            _login = User.objects.filter(username=_user, password=_pass)
            _result = _login.count()
            if _result > 0:
                request.session['username'] = _login[0].username
                request.session['id'] = _login[0].id
                request.session['password'] = _login[0].password
                _statu = {'statu': 1}
            else:
                _statu = {'statu': 0, 'msg': u'用户名或密码错误'}
        else:
            _statu = {'statu': 0, 'msg': u'用户名或密码格式错误'}
        return MyResponse.SendData(_statu)
    return render(request, 'member/member_login.html')


def member_logout(request):
    request.session.flush()
    return HttpResponseRedirect('/member/login/')


# -------------------------------- 后台管理 部分 ----------------

def admin_index(request):
    return render(request, 'member/admin.html')


def admin_usergroup_add(request):
    if request.method == 'POST':
        _form = AddUserGroupForm(request.POST)
        if _form.is_valid():
            _permission = _form.cleaned_data['permission']
            _info = _form.cleaned_data['info']
            print '收到的权限列表:', _permission
            _resultP = MyPermission.read_permission(_permission)
            print '计算后的结果:', _resultP
            UserGroup.objects.create(name=_info, permission=_resultP)
            _dic = {'statu': 1}
            return MyResponse.SendData(_dic)
        else:
            _dic = {'statu': 0, 'form': _form.errors}
            return MyResponse.SendData(_dic)
    else:
        _form = AddUserGroupForm()
    _p_qs = UserPermission.objects.all()
    return render(request, 'member/add_usergroup.html', {'user_permission': _p_qs, 'form': _form})


def list_usergroup(request):
    _qs = UserGroup.objects.all()
    _list = []
    for item in _qs:
        _dic = {'name': item.name, 'permission': item.permission, 'id': item.id}
        _list.append(_dic)
    _result = {'UserGroup': _list}
    return MyResponse.SendData(_result)


def edit_usergroup(request):
    if request.method == 'POST':
        _form = EditUserGroupForm(request.POST)
        if _form.is_valid():
            _permission = _form.cleaned_data['permission']
            _info = _form.cleaned_data['info']
            _id = _form.cleaned_data['id']
            print '收到的权限列表:', _permission
            _resultP = MyPermission.read_permission(_permission)
            print '计算后的结果:', _resultP
            UserGroup.objects.filter(id=_id).update(name=_info, permission=_resultP)
            _dic = {'statu': 1}
            return MyResponse.SendData(_dic)
        else:
            _dic = {'statu': 0, 'form': _form.errors}
            return MyResponse.SendData(_dic)
    _id = request.GET.get('id')
    try:
        _up = UserGroup.objects.get(id=_id)
        _p_qs = UserPermission.objects.all()

    except:
        pass
    return render(request, 'member/edit_usergroup.html', {'UserGroup': _up, 'user_permission': _p_qs})


def admin_user(request):
    _uqs = User.objects.all()
    return render(request, 'member/admin_user.html', {'userlist': _uqs})
