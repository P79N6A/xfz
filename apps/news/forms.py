# -*- coding: utf-8 -*-
# @Time:2018.12.25 15:41
# @Author:Zhang
# @Desc  :
from django import forms
from apps.forms import FormMixin

class PublicCommentForm(forms.Form,FormMixin):
    content = forms.CharField()
    news_id = forms.IntegerField()