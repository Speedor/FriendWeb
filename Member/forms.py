# -*- coding: utf-8 -*-
from django import forms
from .models import User
from django.core import validators

class MemberRegisterForm(forms.ModelForm):
    password_valid = validators.RegexValidator(r'^[a-zA-Z0-9]{6,18}$', u'请出入正确的密码格式，长度为6-18')
    username_valid = validators.RegexValidator(r'^[a-zA-Z0-9\u4e00-\u9fa5]{2,15}$', u'输入正确的用户昵称,长度为2-15')
    email_valid = validators.EmailValidator(u'请出入正确格式的email')

    username = forms.CharField(validators=[username_valid])
    password = forms.CharField(validators=[password_valid])
    email = forms.EmailField(validators=[email_valid])

    class Meta:
        model = User
        fields = ['username','email','password']

class MemberLoginForm(forms.Form):
    password_valid = validators.RegexValidator(r'^[a-zA-Z0-9]{6,18}$', u'请出入正确的密码格式，长度为6-18')
    username_valid = validators.RegexValidator(r'^[a-zA-Z0-9\u4e00-\u9fa5]{2,15}$', u'输入正确的用户昵称,长度为2-15')
    username = forms.CharField(validators=[username_valid])
    password = forms.CharField(validators=[password_valid])

    class Meta:
        model = User
        fields = ['username', 'password']


class AddUserGroupForm(forms.Form):
    info = forms.CharField(max_length=20)
    permission = forms.CharField(min_length=1)

class EditUserGroupForm(forms.Form):
    id = forms.IntegerField()
    info = forms.CharField(max_length=20)
    permission = forms.CharField(min_length=1)