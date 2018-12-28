# -*- coding: utf-8 -*-
# @Time:2018.12.13 19:21
# @Author:Zhang
# @Desc  :

from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('<int:news_id>/',views.news_detail,name='news_detail'),
    path('search/',views.search,name='search'),
    path('list/', views.news_list, name='news_list'),
    path('public_comment/', views.public_comment, name='public_comment'),

    path('public_comment/', views.public_comment, name='public_comment'),

]