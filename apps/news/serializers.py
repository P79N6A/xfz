# -*- coding: utf-8 -*-
# @Time:2018.12.23 21:31
# @Author:Zhang
# @Desc  :
from rest_framework import serializers
from .models import News,NewsCategory,Comment,Banner
from apps.xfzauth.serializers import UserSerializers


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializers()
    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','pub_time','category','author')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializers()
    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields=('id','img_url','priority','link_to')
