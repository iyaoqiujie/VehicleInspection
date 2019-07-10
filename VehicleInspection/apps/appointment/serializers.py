# -*- coding: utf-8 -*-
# Author：Qiujie Yao
# Email: yaoqiujie@gscopetech.com
# @Time: 2019-06-26 14:09

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_redis import cache, get_redis_connection
from .models import AppointmentOrder, AppmntOrderAgg
import logging

User = get_user_model()
myLogger = logging.getLogger('insp.appointment')


class AppointmentOrderSerializer(serializers.ModelSerializer):
    orderuser_mobile = serializers.ReadOnlyField(source='order_user.mobile')
    station_name = serializers.ReadOnlyField(source='station.name')
    created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    code = serializers.IntegerField(default=20000, read_only=True)

    class Meta:
        model = AppointmentOrder
        fields = '__all__'


class AppmntOrderAggSerializer(serializers.ModelSerializer):
    station_name = serializers.ReadOnlyField(source='station.name')
    code = serializers.IntegerField(default=20000, read_only=True)

    class Meta:
        model = AppmntOrderAgg
        fields = '__all__'

