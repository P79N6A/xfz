from django.shortcuts import render, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST
from .cms_forms import EditNewsCategory, WriteNewsForm, AddBannerForm,EditBannerForm,EditNewsForm
from apps.news.models import NewsCategory, News, Banner
from utils import restful
import os
from django.conf import settings
import qiniu
from apps.news.serializers import BannerSerializer

from django.core.paginator import Paginator,Page
from datetime import  datetime
from django.utils.timezone import make_aware
#将字典变成查询字符串
from urllib import parse

# Create your views here.

# 员工成员映射，若不是员工，则重定向到login_url
@staff_member_required(login_url='index')
def index(request):
    return render(request, 'cms/index.html')

class NewsListView(View):
    def get(self,request):

        start = request.GET.get('start')
        end = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category',0) or 0)

        newses=News.objects.select_related('category', 'author')

        if start or end:
            if start:
                #将时间字符串转换为时间元组struct_time
                start_date = datetime.strptime(start,'%Y/%m/%d')
            else:
                start_date = datetime(year=2018,month=6,day=1)
            if end:
                end_date = datetime.strptime(end, '%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))
        if title:
            newses = newses.filter(title__icontains=title)
        if category_id:
            newses = newses.filter(category=category_id)
        #获取当前的页数
        page=int(request.GET.get('page',1))
        #创建总分页对象
        paginator = Paginator(newses,2)
        #当前页对象 object_list获取当前页数据
        page_object = paginator.page(page)

        context_data = self.get_paginate_data(paginator,page_object)

        content = {
            'categories': NewsCategory.objects.all(),
            'newses': page_object.object_list,
            'start':start,
            'end':end,
            'title':title,
            'category_id':category_id,
            'url_query':'&'+parse.urlencode({
                'start':start or '',
                'end':end or '',
                'title':title or '',
                'category':category_id or ''
            })
        }
        content.update(context_data)
        return render(request, 'cms/news_list.html', context=content)

    def get_paginate_data(self, paginator, page_obj, arround_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages
        left_has_more = False
        right_has_more = False

        if current_page <= arround_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - arround_count, current_page)

        if current_page >= num_pages - arround_count-1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + arround_count + 1)

        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages':num_pages,
            'page_obj':page_obj,
        }


class WriteNews(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'cms/write_news.html', context=context)

    def post(self, request):
        form = WriteNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title, desc=desc, thumbnail=thumbnail, content=content, category=category,
                                author=request.user)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())


class EditNewsView(View):
    def get(self,request):
        news_id = request.GET.get('news_id')
        news = News.objects.get(pk=news_id)
        context = {
            'news':news,
            'categories':NewsCategory.objects.all(),

        }
        return render(request,'cms/write_news.html',context=context)

    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get('pk')
            category = NewsCategory.objects.get(id=category_id)
            News.objects.filter(pk=pk).update(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

@require_POST
def delete_news(request):
    '''新闻删除'''
    news_id = request.POST.get('news_id')
    print('删除了新闻id为',news_id)
    #News.objects.filter(pk=news_id).delete()
    return restful.ok()



@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'cms/news_category.html', context=context)


@require_POST
def add_news_category(request):
    '''添加新闻分类'''
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在！')


@require_POST
def edit_news_category(request):
    form = EditNewsCategory(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message="该新闻分类不存在!")
    else:
        return restful.params_error(message=form.get_errors())


@require_POST
def delete_news_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message="该分类不存在！")


@require_POST
def upload_file(request):
    '''上传到本地media文件夹'''
    file = request.FILES.get('file')
    name = file.name
    file_path = os.path.join(settings.MEDIA_ROOT, name)
    with open(file_path, 'wb')as fp:
        for chunk in file.chunks():
            fp.write(chunk)

    # http://127.0.0.1:8000+/media/
    img_url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return restful.result(data={'url': img_url})


@require_GET
def qntoken(request):
    '''上传到7牛服务器'''
    # 自己的
    # access_key='_jVML1LKmI7cM84-Le549f7OwWab7e-hZD-4Nf6W'
    # secret_key='ssWppsaMibQkd1XC-q0Y4WPVUXFhAO4EoVHwJg5S'

    access_key = 'M4zCEW4f9XPanbMN-Lb9O0S8j893f0elezAohFVL'
    secret_key = '7BKV7HeEKM3NDJk8_1_C89JI3SMmeUIAIatz19d4'
    # 存储空间
    bucket = 'hyvideo'
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket)

    return restful.result(data={'token': token})


def banners(request):
    '''显示轮播图页面'''
    return render(request, 'cms/banners.html')

def banner_list(request):
    '''传递给art-template banner数据'''
    banners = Banner.objects.all()
    serialize = BannerSerializer(banners,many=True)
    return restful.result(data=serialize.data)



def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        img_url = form.cleaned_data.get('img_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority, img_url=img_url, link_to=link_to)
        return restful.result(data={'banner_id': banner.pk})
    else:
        return restful.method_error(message=form.get_errors())

def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()

def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        priority = form.cleaned_data.get('priority')
        img_url = form.cleaned_data.get('img_url')
        link_to = form.cleaned_data.get('link_to')

        Banner.objects.filter(pk=pk).update(priority=priority,img_url=img_url,link_to=link_to)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())
