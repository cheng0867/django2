#coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from hashlib import sha1
from models import *
from . import user_decorator

# Create your views here.
def register(request):
    context = {
        'title':'注册'
    }
    return render(request,'df_user/register.html',context)

def register_exist(request):
    # 获取注册页发来的ajax的get请求中的uname
    uname = request.GET.get('uname')
    # 获取在数据库中查询的数量,有则1,没有则0
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def register_handle(request):
    # 获取post
    post_obj = request.POST
    uname = post_obj.get('user_name')
    upwd = post_obj.get('pwd')
    uemail = post_obj.get('email')
    # 使用sha1加密
    s1 = sha1()
    s1.update(upwd)
    spwd = s1.hexdigest()
    # 实例化userinfo
    user = UserInfo()
    user.uname = uname
    user.upwd = spwd
    user.uemail = uemail
    user.save()
    return redirect('/user/login/')

def login(request):
    # 如果记住密码,则获取保存在cookie中的用户名
    uname = request.COOKIES.get('uname','')
    context = {
        'title':'用户登录',
        'uanme':uname,
        'error_name':0,
        'error_pwd':0,
    }
    return render(request,'df_user/login.html',context)

def login_handle(request):
    # 获取post请求
    post_obj = request.POST
    uname = post_obj.get('username')
    upwd = post_obj.get('pwd')
    uremember = post_obj.get('remember')
    # 在数据库中查询匹配的用户名
    user = UserInfo.objects.filter(uname=uname)

    # 判断用户名是否存在
    if len(user) == 1:
        # 准备sha1
        s1 = sha1()
        s1.update(upwd)
        # 判断加密后的密码,与数据库中的密码是否匹配
        if s1.hexdigest() == user[0].upwd:
            # 获取cookie中的url,有则给值,无则赋空
            url = request.COOKIES.get('url','/')
            # 定义response对象
            rd = redirect(url)
            # 使url过期
            rd.set_cookie('url','',max_age=-1)
            # 判断是否记住用户名
            if uremember == 1:
                rd.set_cookie('uname',uname)
            else:
                rd.set_cookie('uname','',max_age=-1)
            # 将id和用户名写入session
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return rd
        # 密码错误,返回到登录页
        else:
            context = {
                'title':'用户登录',
                'uname':uname,
                'error_name':0,
                'error_pwd':1,
            }
            return render(request,'df_user/login.html',context)
    # 用户名错误,返回到登录页
    else:
        context = {
            'title':'用户登录',
            'uanme':uname,
            'error_name':1,
            'error_pwd':0,
        }
        return render(request,'df_user/login.html',context)

def logout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def info(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    context = {
        'title':'用户中心',
        'page_name':1,
        'uname':user.uname,
        'uphone':user.uphone,
        'uaddress':user.uaddress,
    }
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request):
    context = {
        'title':'用户中心',
        'page_name':1,
    }
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    # 找到数据库中的当前用户
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 如果是post请求
    if request.method == 'POST':
        # 将post请求的数据写入当前对应的数据库中
        post_obj = request.POST
        user.ushou = post_obj.get('ushou')
        user.uaddress = post_obj.get('uaddress')
        user.uyoubian = post_obj.get('uyoubian')
        user.uphone = post_obj.get('uphone')
        user.save()
    context = {
        'title':'用户中心',
        'page_name':1,
        'user':user,
    }
    return render(request,'df_user/user_center_site.html',context)