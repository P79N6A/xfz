# -*- coding: utf-8 -*-
# @Time:2018.12.14 19:04
# @Author:Zhang
# @Desc  :
from django.shortcuts import redirect,render
from .models import *
import time
from django.conf import settings
import os
import hmac,hashlib
from utils import restful
from apps.xfzauth.decorators import *

def course_index(request):
    content = {
        'course':Course.objects.all()
    }
    return render(request,'course/course_index.html',context=content)

def course_detail(request,course_id):
    #try
    course = Course.objects.get(pk=course_id)
    content = {
        'course':course
    }
    return render(request,'course/course_detail.html',context=content)

def course_token(request):
    file = request.GET.get('video')

    expiration_time = int(time.time()) + 2 *60 *60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension,'')

    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id,expiration_time).encode('utf-8')
    signature = hmac.new(key,message,digestmod=hashlib.sha256).hexdigest()
    token = '{0}.{1}.{2}'.format(signature,USER_ID,expiration_time)
    return restful.result(data={'token':token})


@xfz_login_required
def course_oder(request,course_id):
    course = Course.objects.get(pk=course_id)
    order = CourseOrder.objects.create(course=course,buyer=request.user,status=1,amount=course.price)
    content = {
        'course':course,
        'order':order,
    }
    return render(request,'course/course_order.html',context=content)

