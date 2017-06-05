#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    typelist = TypeInfo.objects.all()
    list = []
    for type in typelist:
        list.append({
            'type':type,
            'click_list':type.goodsinfo_set.order_by('-gclick')[0:3],
            'new_list':type.goodsinfo_set.order_by('-id')[0:4],
        })
    context = {
        'title':'首页',
        'list':list,
    }
    return render(request,'df_goods/index.html',context)

def list(request,tid,pindex,orderby):
    # 获取对应分类
    gtype = TypeInfo.objects.get(id=int(tid))
    # 获取对应分类最新数据
    new_list = gtype.goodsinfo_set.order_by('-id')[0:2]
    # 获取对应分类所有数据
    goods_list = GoodsInfo.objects.filter(gtype_id=int(tid))
    # 排序规则
    # 最新
    if orderby == '1':
        goods_list = goods_list.order_by('-id')
    # 价格
    elif orderby == '2':
        goods_list = goods_list.order_by('-gprice')
    # 人气
    else:
        goods_list = goods_list.order_by('-gclick')

    paginator = Paginator(goods_list,10)
    pindex = int(pindex)
    if pindex <= 0:
        pindex = 1
    elif pindex > paginator.num_pages:
        pindex = paginator.num_pages
    page = paginator.page(pindex)
    context = {
        'title':'商品列表',
        'page':page,
        'tid':tid,
        'new_list':new_list,
        'gtype':gtype,
        'orderby':orderby,
    }
    return render(request,'df_goods/list.html',context)

def detail(request,gid):
    goods = GoodsInfo.objects.get(id=gid)
    goods.gclick = goods.gclick+1
    goods.save()
    # 当前商品对应的分类,最新的两个商品
    new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title':'商品详情',
        'goods':goods,
        'new_list':new_list,
    }
    return render(request,'df_goods/detail.html',context)

from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        extra = super(MySearchView, self).extra_context()
        extra['title']=self.request.GET.get('q')
        return extra