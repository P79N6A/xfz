# -*- coding: utf-8 -*-
# @Time:2018.12.22 15:28
# @Author:Zhang
# @Desc  :
from django import forms
from apps.forms import FormMixin
from apps.news.models import News, Banner
from apps.course.models import *

class EditNewsCategory(forms.Form, FormMixin):
    pk = forms.IntegerField(error_messages={"required": "必须传入分类id"})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class EditNewsForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    pk = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['category','author','pub_time']




class AddBannerForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Banner
        fields = ['priority', 'img_url', 'link_to']

class EditBannerForm(forms.ModelForm,FormMixin):
    pk= forms.IntegerField()
    class Meta:
        model = Banner
        fields=['priority', 'img_url', 'link_to','pk']


class PubCourseForm(forms.ModelForm,FormMixin):
    teacher_id = forms.IntegerField()
    category_id = forms.IntegerField()
    class Meta:
        model = Course
        exclude = ('category','teacher',)