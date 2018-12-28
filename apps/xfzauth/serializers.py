# -*- coding: utf-8 -*-
# @Time:2018.12.23 21:38
# @Author:Zhang
# @Desc  :
from rest_framework import serializers
from .models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'telephone', 'username', 'email', 'is_staff', 'is_active')
