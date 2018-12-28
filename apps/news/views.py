from django.shortcuts import render
from .models import News, NewsCategory
from django.conf import settings
from utils import restful
from .serializers import *
from django.http import Http404
from . import forms
from .models import *
from django.contrib.auth.decorators import login_required
from apps.xfzauth.decorators import xfz_login_required

# Create your views here.
def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('category', 'author').all()[0:count]
    categories = NewsCategory.objects.all()
    info = Banner.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
        'banners':info,
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    # 通过p参数来指定要获取第几页数据，并且这个p参数是通过查询字符串传递
    # /news/list/?p=1默认
    page = int(request.GET.get('p', 1))
    # 默认为0代表不进行任何分类
    category_id = int(request.GET.get('category_id', 0))
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        newses = News.objects.select_related('category', 'author').all()[start:end]
    else:
        # .values() queryset转换为列表字典
        newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
    # 放入serializer中序列化，queryset对象需要传递many=True
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    # {'id':1,'title':'abc','category':{'id':1,'name':'热点'}}
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        #根据外键查询分类与作者，
        news = News.objects.select_related('category', 'author').prefetch_related('comments__author').get(pk=news_id)

        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        return Http404

@xfz_login_required
def public_comment(request):
    '''发布评论'''
    form = forms.PublicCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')

        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        # 对象放入serializer中序列化
        serializer = CommentSerializer(comment)
        return restful.result(data=serializer.data)

    else:
        return restful.params_error(message=form.get_errors())



def search(request):
    return render(request, 'search/search.html')
