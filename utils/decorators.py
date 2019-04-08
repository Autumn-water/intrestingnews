from django.contrib.auth.models import Permission, ContentType
from functools import wraps

from utils import json_status
from .json_status import un_auth_error
from django.shortcuts import redirect, reverse


# 装饰器 === 闭包 + 高阶函数
def ajax_login_required(view_func):
    @wraps(view_func)  # 保证原函数的特性
    def wrapper(request, *args, **kwargs):
        # 如果说 用户登录了 就跳过 什么方法可以判断用户是否登录
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            # 判断是不是 ajax 请求
            if request.is_ajax():
                return un_auth_error(message="请先登录")
            # 如果不是 ajax
            return redirect(reverse("account:login"))
    return wrapper


"""
@ajax_login_required(xxx)  ==> a = a(ajax_login_required(a))
def a():
    pass
"""


# 权限装饰器 是可以传参的 这个装饰器是要传参 @r(xx) 传一个模型名字
def user_permission_required(model_name):
    # 用于接收视图函数
    def wrapper(view_func):
        @wraps(view_func)
        def func(request, *args, **kwargs):
            # 根据对应的模型找到 对应的content_type
            content_type = ContentType.objects.get_for_model(model_name)
            # 找到权限 permission 是多个 每个模型都有四个权限（add/change/delete/view） 模型找的
            permissions = Permission.objects.filter(content_type=content_type)
            print('============')
            print(permissions)
            print('===============================')
            for permission in permissions:
                print(permission)
            print('============')
            # 拼接权限 app名字.权限名字 ==> news.change_news
            # 每一个 permission Can change news tag	6	change_newstag
            # app_label ============== app的名字
            code_name = [content_type.app_label + '.' + permission.codename for permission in permissions]
            print('code_name{}'.format(code_name))
            # 判断是否具有权限 是要判断一个用户是否具有权限  has_perms （只能接收`app_label.权限`） news.change_news
            # 返回有权限 就有值  没有权限 就没值
            res = request.user.has_perms(code_name)
            if res:
                return view_func(request, *args, **kwargs)
            return json_status.un_auth_error(message='权限不足')
        return func
    return wrapper


# 是不是超级管理员
def is_super_user_required(view_func):
    @wraps(view_func)
    def func(request, *args, **kwargs):
        # 怎么样表示它是一个超级管理员 逻辑
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return json_status.un_auth_error(message="你不是炒鸡管理员")
    return func
