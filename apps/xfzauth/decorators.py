# -*- coding: utf-8 -*-
# @Time:2018.12.25 19:30
# @Author:Zhang
# @Desc  :
from utils import restful
from django.shortcuts import redirect,reverse
def xfz_login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.params_unauth(message='请先登陆!')
            else:
                return redirect('/')
    return wrapper