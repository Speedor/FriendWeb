# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import *


# 注册验证，基于模型表的定义来校验
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


# 登入表单
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, label=u'用户')
    # 密码输入，隐藏输入字符，且用星号标识
    password = forms.CharField(max_length=20, label=u'密码')


# 添加博客分类表单
class AddSortForms(forms.ModelForm):
    sort_name = forms.CharField(label=u'分类名称')

    class Meta:
        model = SortTable
        fields = ['sort_name']


# 编辑博客分类表单
class EditSortForms(forms.ModelForm):
    sort_name = forms.CharField(label=u'分类名称', min_length=2)
    id = forms.IntegerField()

    class Meta:
        model = SortTable
        fields = ['sort_name']


# 添加博文表单
class AddBlogForms(forms.ModelForm):
    sort_id = forms.IntegerField()

    class Meta:
        model = Blog
        fields = ['title', 'content']


# 图片上传表单
class ImgForm(forms.ModelForm):
    class Meta:
        model = PicTable
        fields = ['pic']


# 编辑博客
class EditBlogForms(forms.ModelForm):
    sort_id = forms.IntegerField()

    class Meta:
        model = Blog
        fields = ['title', 'content']