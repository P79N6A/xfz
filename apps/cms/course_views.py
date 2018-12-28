# -*- coding: utf-8 -*-
# @Time:2018.12.27 15:58
# @Author:Zhang
# @Desc  :
from django.shortcuts import render, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_GET, require_POST
from utils import restful
import os
from apps.course.models import *
from django.conf import settings
from django.core.paginator import Paginator, Page
from datetime import datetime
from django.utils.timezone import make_aware
# 将字典变成查询字符串
from urllib import parse
from .cms_forms import *


# def pub_coures(request):
#     return render(request, 'cms/pub_course.html')
#

class PubClassView(View):
    def get(self, request):
        context = {
            'category': CourseCategory.objects.all(),
            'teacher': Teacher.objects.all()
        }
        return render(request, 'cms/pub_course.html', context=context)

    def post(self, request):
        form = PubCourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get('profile')
            teacher_id = form.cleaned_data.get('teacher_id')

            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)

            Course.objects.create(title=title,category=category,video_url=video_url,cover_url=cover_url,price=price,duration=duration,profile=profile,teacher=teacher)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())
