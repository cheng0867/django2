#coding=utf-8
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title':'首页'
    }
    return render(request,'df_goods/index.html',context)