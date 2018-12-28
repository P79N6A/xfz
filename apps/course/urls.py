# -*- coding: utf-8 -*-
# @Time:2018.12.14 19:04
# @Author:Zhang
# @Desc  :

from django.urls import path
from . import views

app_name = 'course'

urlpatterns = [
    path('',views.course_index,name='course_index'),
    path('<int:course_id>/',views.course_detail,name='course_detail'),
    path('course_token/', views.course_token, name='course_token'),
    path('course_oder/<int:course_id>', views.course_oder, name='course_oder'),

]