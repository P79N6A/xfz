# -*- coding: utf-8 -*-
# @Time:2018.12.13 21:11
# @Author:Zhang
# @Desc  :
from django.urls import path
from . import views
app_name = 'xfzauth'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('img_captcha/', views.img_captcha, name='img_captcha'),
    path('sms_captcha/', views.sms_captcha, name='sms_captcha'),

    path('memcache_test/', views.memcache_test, name='memcache_test'),

    path('register/', views.register, name='register'),

]