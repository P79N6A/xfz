# -*- coding: utf-8 -*-
# @Time:2018.12.14 19:19
# @Author:Zhang
# @Desc  :
from django.urls import path
from . import views
app_name = 'payinfo'

urlpatterns = [
    path('',views.payinfo,name='payinfo' ),

]