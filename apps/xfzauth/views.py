# -*- coding: utf-8 -*-
# @Time:2018.12.13 20:36
# @Author:Zhang
# @Desc  :

from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,ResgisterForm
from django.http import JsonResponse
from utils import restful
from django.shortcuts import redirect,reverse,HttpResponse
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from django.http import request
from django.core.cache import cache
from utils.dysms_python import aliyunsm
from utils import restful

from django.contrib.auth import get_user_model

#会去读取setting中的AUTH_USER_MODEL
User = get_user_model()


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,username=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    #2周过期
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                    #{'code':200,'message':'(错误信息)','data':'{(用户数据)}'}
                return restful.ok()

            else:
                return restful.params_unauth(message='您的账号已被冻结！')

        else:
            return restful.params_error(message='手机号或密码错误！',)
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors,)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def img_captcha(request):
    text,image = Captcha.gene_code()
    #BytesIO:相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    #调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    #将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    #从BytesIO的管道中，读取图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()
    #设置memcache缓存值
    cache.set(text.lower(),text.lower(),5*60)

    return response



def sms_captcha(request):
    #电话号码
    telephone = request.GET.get('telephone')
    #随机验证码
    code = Captcha.gene_text()

    print(telephone)
    # 手机号为key,code为value
    cache.set(telephone,code,5*60)
    res = aliyunsm.send_sms(telephone,'baxu',template_code=code)
    print('xfzauth:views-line89,发送的短信验证码：',code)
    return restful.ok()

#
def memcache_test(request):
    cache.set('1','zhjng',1)
    res = cache.get('1')
    print(res)
    return HttpResponse(res)


@require_POST
def register(request):
    form = ResgisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request,user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())
