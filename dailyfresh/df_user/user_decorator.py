#coding=utf-8
from django.shortcuts import redirect

# 定义登录装饰器
def login(func):
    def login_fun(request,*args,**kwgs):
        # 如果已经登录,返回当前页面
        if request.session.has_key('user_id'):
            return func(request,*args,**kwgs)
        else:
            rd = redirect('/user/login/')
            rd.set_cookie('url',request.get_full_path())
            return rd
    return login_fun