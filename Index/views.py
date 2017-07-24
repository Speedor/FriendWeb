# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user
import json
import os
from django.conf import settings
from django.template.loader import render_to_string
# ================================================================== 用户视图部分
# 用户注册视图
def register(request):
    if request.method == 'POST':
        _form = RegisterForm(request.POST)
        if _form.is_valid():
            _username = _form.cleaned_data['username']
            _email = _form.cleaned_data['email']
            _password = _form.cleaned_data['password']
            User.objects.create_user(_username, _email, _password)
            return HttpResponseRedirect('/login/')
    else:
        _form = RegisterForm()
    return render(request, 'register.html', {"form": _form})


# 登入视图
def log_in(request):
    if request.method == 'POST':
        # 实例化一个登入表单
        _form = LoginForm(request.POST)
        # 表单验证成功
        if _form.is_valid():
            # 取用表单字段的安全值
            _username = _form.cleaned_data['username']
            _password = _form.cleaned_data['password']
            # 调用框架下 authenticate 方法，验证用户名和密码的正确性
            # 正确，_user将是一个 User 表的一个用户
            # 错误，_user 存储着None
            _user = authenticate(username=_username, password=_password)
            # 判断 _user 非 None, 即判断用户名密码有效
            if _user is not None:
                # 判断用户是否是活跃的，当然我们没有去设置用户锁闭状态
                if _user.is_active:
                    # 调用django框架的 login方法登入
                    login(request, _user)
                    # 成功登入后，跳转到博客管理中心
                    return HttpResponseRedirect('/manage/')
            else:
                # 如果失败，使用 add_error方法，添加错误消息
                _form.add_error("password", u'用户或密码错误')
    else:
        # 如果不是post数据，说明表单初始化呈现
        _form = RegisterForm()
    # 将带着表单数据的界面回馈显示
    return render(request, 'log_in.html', {"form": _form})


# 退出视图
def log_out(request):
    # 调用django框架方法，用户退出
    logout(request)
    # 跳转到登入界面
    return HttpResponseRedirect('/login/')


# ================================================================================ 管理视图部分
# 管理中心视图
def manage(request):
    _user = get_user(request)
    _qs_sort = SortTable.objects.all()
    _qs_blog = Blog.objects.all()
    return render(request, 'manage.html', {'sort_list': _qs_sort, "user": _user, 'blog_list': _qs_blog})


# ====================================================================  分类管理部分
# 添加博客分类
def add_sort(request):
    if request.method == 'POST':
        _form = AddSortForms(request.POST)
        if _form.is_valid():
            _form.save()
            return HttpResponseRedirect("/manage/")
    _form = AddSortForms()
    return render(request, 'add_sort.html', {'form': _form})


# 编辑分类
def edit_sort(request):
    if request.method == "POST":
        _form = EditSortForms(request.POST)
        if _form.is_valid():
            _id = _form.cleaned_data['id']
            _name = _form.cleaned_data['sort_name']
            SortTable.objects.filter(id=_id).update(sort_name=_name)
            return HttpResponseRedirect("/manage/")
        return render(request, 'edit_sort.html', {'form': _form})
    else:
        _id = request.GET.get('id')
        _sort = SortTable.objects.get(id=_id)
        return render(request, 'edit_sort.html', {'sort': _sort})


# 删除博文分类
def del_sort(request):
    _id = request.GET.get('id')
    SortTable.objects.filter(id=_id).delete()
    return HttpResponseRedirect('/manage/')


# ========================================================================== 博文管理
# 添加博文
def add_blog(request):
    _qs_sort = SortTable.objects.all()
    if request.method == 'POST':
        _form = AddBlogForms(request.POST)
        if request.session.get('pic_id') is not None:
            if _form.is_valid():
                _user = get_user(request)
                _sort_id = _form.cleaned_data['sort_id']
                _title = _form.cleaned_data['title']
                _content = _form.cleaned_data['content']
                _pic = request.session.get('pic_id')

                Blog.objects.create(pic_id=_pic, user_id=_user.id, sort_id=_sort_id, title=_title, content=_content)

                _dic = {"status": 1}
                _json = json.dumps(_dic)
                return HttpResponse(_json, content_type='application/json')
        else:
            _form.add_error("pic", u"未上传图片")

        return render(request, 'add_blog.html', {'sort_list': _qs_sort, "form": _form})
    return render(request, 'add_blog.html', {'sort_list': _qs_sort})


# 上传图片
def upload(request):
    if request.method == 'POST':
        _form = ImgForm(request.POST, request.FILES)
        if _form.is_valid():
            _pic = _form.save()
            _id = PicTable.objects.get(pic=_pic.pic).id
            request.session['pic_id'] = _id
            _status = {'is_valid': True, 'name': _pic.pic.name, 'url': _pic.pic.url}
        else:
            _status = {'is_valid': False, 'msg':_form.errors}
        _json = json.dumps(_status)
        return HttpResponse(_json, content_type='application/json')


# 显示博客详情
def detail_blog(request):
    _id = request.GET.get('id')
    _blog = Blog.objects.get(id=_id)
    return render(request, 'detail_blog.html', {'blog': _blog})


#  编辑博文
def edit_blog(request):
    if request.method == "POST":
        _id = request.POST.get('id')
        _form = EditBlogForms(request.POST)
        if _form.is_valid():
            _user = get_user(request)
            _user_id = _user.id
            _sort_id = _form.cleaned_data['sort_id']
            _title = _form.cleaned_data['title']
            _content = _form.cleaned_data['content']

            Blog.objects.filter(id=_id).update(user_id=_user_id, sort_id=_sort_id, title=_title, content=_content)
            _dic = {"status": 1}
            _json = json.dumps(_dic)
            return HttpResponse(_json, content_type='application/json')
        return render(request, 'edit_blog.html', {'form': _form})
    else:
        _id = request.GET.get('id')
        _blog = Blog.objects.get(id=_id)
        _qs_sort = SortTable.objects.all()
        return render(request, 'edit_blog.html', {'blog': _blog, "sort_list": _qs_sort})


# 删除博文
def del_blog(request):
    _id = request.GET.get('id')
    Blog.objects.filter(id=_id).delete()
    return HttpResponseRedirect('/manage/')

# =========================================  优化部分
def index(request):
    _qs_sort = SortTable.objects.all()
    _qs_blog = Blog.objects.all()
    return render(request, 'index.html', {'sort_list': _qs_sort, 'blog_list': _qs_blog})

'''
#  ==================================== 默认首页之 非 缓存原始版代码 开始  ====================================
def index(request):
    _qs_sort = SortTable.objects.all()
    _qs_blog = Blog.objects.all()
    return render(request, 'index.html', {'sort_list': _qs_sort, 'blog_list': _qs_blog})

   ==================================== 默认首页之 非 缓存原始版代码 结束  ====================================
'''
'''
 ==================================== 全网页缓存 代码的开始 ====================================
def read_data(request):
    _user = get_user(request)
    _qs_sort = SortTable.objects.all()
    _qs_blog = Blog.objects.all()
    return {'blog_list': _qs_blog, 'user': _user,'sort_list': _qs_sort}


def show_page_from_template(request):
    return render(request, 'index.html',read_data(request) )


def FreshCache(request):
    static_html = os.path.join(settings.BASE_DIR, 'CacheDir\Cached.html')
    content = render_to_string('index.html', read_data(request))
    _file = open(static_html, 'w')
    _file.write(content.encode("utf8"))
    _file.close()


def show_page_from_cache(request):
    static_html = os.path.join(settings.BASE_DIR, 'CacheDir\Cached.html')
    if not os.path.exists(static_html):
        FreshCache(request)
    return render(request, 'Cached.html')


def index(request):
    if request.GET.get("logout") == 't':
        FreshCache(request)
    try:
        id = request.session.get('user')
        if id is not None:
            return show_page_from_template(request)
        else:
            return show_page_from_cache(request)
    except AttributeError:
        return show_page_from_cache(request)


======================================   全网页缓存代码的结束 ====================================
'''
'''
======================================   json数据缓存，handlerbars前端框架渲染模版 开始 ====================================

def FreshCache(request):
    static_html = os.path.join(settings.BASE_DIR, 'CacheDir\Cached.json')
    _qs_blog = Blog.objects.all()
    _result = []
    for blog in _qs_blog:
        _dic = {"id": blog.id,
                "url": blog.pic.pic.url,
                "title": blog.title
                }
        _result.append(_dic)
    _obj = {"list":_result}
    json_string = json.dumps(_obj)
    static_file = open(static_html,'w')
    static_file.write(json_string.encode("utf8"))
    static_file.close()


def index(request):
    _user = get_user(request)
    _qs_sort = SortTable.objects.all()
    return render(request, 'index_json.html',{'user': _user,'sort_list': _qs_sort})


def index_api(request):
    static_html = os.path.join(settings.BASE_DIR, 'CacheDir\Cached.json')

    if not os.path.exists(static_html):
        FreshCache(request)
    try:
        file_object = open(static_html)
        json_string_from_file = file_object.read()
        return HttpResponse(json_string_from_file, content_type='application/json')
    except IOError:
        json_obj = {"status": 0}
        json_string_from_file = json.dumps(json_obj)
        return HttpResponse(json_string_from_file, content_type='application/json')
======================================   json数据缓存，handlerbars前端框架渲染模版 结束 ====================================
'''