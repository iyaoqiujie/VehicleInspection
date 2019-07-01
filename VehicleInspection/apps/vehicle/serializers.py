# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-27 23:22

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_redis import cache, get_redis_connection
from .models import Vehicle
import logging

User = get_user_model()
myLogger = logging.getLogger('insp.vehicle')


class VehicleSerializer(serializers.ModelSerializer):
    bounduser_mobile = serializers.ReadOnlyField(source='bound_user.mobile')
    code = serializers.IntegerField(default=20000, read_only=True)

    class Meta:
        model = Vehicle
        fields = '__all__'
